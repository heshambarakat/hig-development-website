import uuid

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.translation import get_language
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from apps.integrations.meta import send_meta_lead_event
from apps.integrations.sheets import sync_lead_to_google_sheet
from apps.leads.forms import LeadForm
from apps.tracking.models import TrackingEvent
from apps.tracking.views import get_or_create_session


@require_POST
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def submit_lead(request):
    data = request.POST.copy()
    session = get_or_create_session(request)
    data.setdefault("language", get_language() or "ar")
    data.setdefault("page_url", request.META.get("HTTP_REFERER", ""))
    if request.COOKIES.get("hig_marketing_consent") == "yes":
        data.setdefault("fbp", request.COOKIES.get("_fbp", ""))
        data.setdefault("fbc", request.COOKIES.get("_fbc", ""))
    for field in ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"):
        if not data.get(field):
            data[field] = getattr(session, field, "")

    form = LeadForm(data)
    if not form.is_valid():
        messages.error(request, "Please check your details and try again.")
        referer = request.META.get("HTTP_REFERER", "")
        fallback = f"/{data.get('language') if data.get('language') in {'ar', 'en'} else 'ar'}/"
        return redirect(referer if url_has_allowed_host_and_scheme(referer, {request.get_host()}) else fallback)

    lead = form.save(commit=False)
    try:
        if data.get("event_id"):
            lead.event_id = uuid.UUID(data["event_id"])
    except (ValueError, TypeError, AttributeError):
        pass
    lead.visitor_session = session
    lead.save()

    TrackingEvent.objects.create(
        visitor_session=session,
        event_type="lead_submit",
        page_url=lead.page_url,
        project_name=lead.project,
        metadata={"lead_id": lead.pk, "event_id": str(lead.event_id)},
    )

    try:
        sync_lead_to_google_sheet(lead)
    except Exception as exc:
        lead.google_sheet_synced = False
        lead.google_sheet_status = "sync_failed"
        lead.google_sheet_error = str(exc)[:1000]
        lead.save(update_fields=["google_sheet_synced", "google_sheet_status", "google_sheet_error"])
    try:
        send_meta_lead_event(lead, request)
    except Exception:
        pass

    if settings.ADMIN_EMAIL:
        send_mail(
            subject=f"New HIG lead: {lead.project or 'Website'}",
            message=f"Name: {lead.name}\nPhone: {lead.phone}\nProject: {lead.project}\nPage: {lead.page_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

    language = lead.language if lead.language in {"ar", "en"} else "ar"
    return redirect(f"/{language}/thank-you/")
