import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from apps.tracking.models import TrackingEvent, VisitorSession


def get_or_create_session(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    session, created = VisitorSession.objects.get_or_create(
        session_key=session_key,
        defaults={
            "first_landing_page": request.build_absolute_uri("/") if request.path == "/" else request.META.get("HTTP_REFERER", ""),
            "device_browser": request.META.get("HTTP_USER_AGENT", "")[:220],
            "marketing_consent": request.COOKIES.get("hig_marketing_consent") == "yes",
        },
    )
    if not created and request.COOKIES.get("hig_marketing_consent") == "yes" and not session.marketing_consent:
        session.marketing_consent = True
        session.save(update_fields=["marketing_consent", "updated_at"])
    return session


@csrf_exempt
@require_POST
@ratelimit(key="ip", rate="120/m", method="POST", block=True)
def track_event(request):
    if len(request.body) > 16384:
        return JsonResponse({"ok": False, "error": "Payload too large"}, status=413)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)

    event_type = payload.get("event_type")
    if event_type not in dict(TrackingEvent.EVENT_TYPES):
        return JsonResponse({"ok": False, "error": "Invalid event type"}, status=400)

    session = get_or_create_session(request)
    page_url = payload.get("page_url", "")[:500]
    metadata = payload.get("metadata", {})
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict) or len(json.dumps(metadata)) > 4096:
        return JsonResponse({"ok": False, "error": "Invalid metadata"}, status=400)
    duration_seconds = metadata.get("duration_seconds")
    if duration_seconds is not None and (
        not isinstance(duration_seconds, int) or duration_seconds < 0 or duration_seconds > 86400
    ):
        return JsonResponse({"ok": False, "error": "Invalid duration"}, status=400)

    if payload.get("first_landing_page") and not session.first_landing_page:
        session.first_landing_page = payload["first_landing_page"][:500]
    for field in ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"):
        value = str(payload.get(field, ""))[:160]
        if value and not getattr(session, field):
            setattr(session, field, value)
    if page_url:
        session.last_page_url = page_url
    session.save(update_fields=[
        "first_landing_page", "last_page_url", "utm_source", "utm_medium",
        "utm_campaign", "utm_content", "utm_term", "updated_at",
    ])

    TrackingEvent.objects.create(
        visitor_session=session,
        event_type=event_type,
        page_url=page_url,
        project_name=payload.get("project_name", "")[:160],
        metadata=metadata,
        duration_seconds=duration_seconds if isinstance(duration_seconds, int) else None,
    )
    return JsonResponse({"ok": True})
