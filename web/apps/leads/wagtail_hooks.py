from django.db.models import Count
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.urls import path
from django.views.generic import TemplateView
from wagtail.admin.menu import MenuItem
from wagtail.admin.auth import require_admin_access
from wagtail import hooks

from apps.leads.models import Lead
from apps.tracking.models import TrackingEvent


@method_decorator(require_admin_access, name="dispatch")
class LeadListView(PermissionRequiredMixin, TemplateView):
    template_name = "wagtailadmin/leads_list.html"
    permission_required = "leads.view_lead"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leads"] = Lead.objects.select_related("visitor_session")[:100]
        context["total_leads"] = Lead.objects.count()
        context["new_leads"] = Lead.objects.filter(status="new").count()
        context["synced_leads"] = Lead.objects.filter(google_sheet_synced=True).count()
        context["tracked_leads"] = Lead.objects.exclude(visitor_session=None).count()
        return context


@method_decorator(require_admin_access, name="dispatch")
class LeadDetailView(PermissionRequiredMixin, TemplateView):
    template_name = "wagtailadmin/lead_detail.html"
    permission_required = "leads.view_lead"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = get_object_or_404(Lead.objects.select_related("visitor_session"), pk=kwargs["pk"])
        context["lead"] = lead
        journey_events = list(
            lead.visitor_session.events.order_by("occurred_at")
            if lead.visitor_session_id
            else []
        )
        context["journey_events"] = journey_events
        page_times = {}
        project_pages = []
        cta_clicks = []
        max_scroll_depth = 0
        map_interactions = 0
        event_labels = {
            "session_started": "بدأ الزيارة",
            "page_view": "شاهد صفحة",
            "project_view": "شاهد مشروعًا",
            "map_interaction": "تفاعل مع الخريطة",
            "scroll_depth": "تصفّح محتوى الصفحة",
            "cta_click": "ضغط على زر",
            "lead_form_start": "بدأ ملء النموذج",
            "lead_submit": "أرسل بياناته",
        }
        if lead.visitor_session_id:
            for event in journey_events:
                if event.page_url and event.duration_seconds:
                    page_times[event.page_url] = page_times.get(event.page_url, 0) + event.duration_seconds
                if event.event_type == "project_view" and event.page_url not in project_pages:
                    project_pages.append(event.page_url)
                if event.event_type == "scroll_depth":
                    max_scroll_depth = max(max_scroll_depth, int(event.metadata.get("depth", 0) or 0))
                if event.event_type == "cta_click":
                    cta_clicks.append(event.metadata.get("text") or event.metadata.get("href") or "زر غير مسمى")
                if event.event_type == "map_interaction":
                    map_interactions += 1
                event.friendly_label = event_labels.get(event.event_type, event.get_event_type_display())
                event.detail_text = _event_detail(event)
        context["page_times"] = page_times
        context["project_pages"] = project_pages
        context["cta_clicks"] = cta_clicks
        context["max_scroll_depth"] = max_scroll_depth
        context["map_interactions"] = map_interactions
        context["event_count"] = len(journey_events)
        context["first_event"] = journey_events[0] if journey_events else None
        context["last_event"] = journey_events[-1] if journey_events else None
        return context


@method_decorator(require_admin_access, name="dispatch")
class TrackingSummaryView(PermissionRequiredMixin, TemplateView):
    template_name = "wagtailadmin/tracking_summary.html"
    permission_required = "tracking.view_trackingevent"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = (
            TrackingEvent.objects.values("event_type")
            .annotate(total=Count("id"))
            .order_by("event_type")
        )
        context["recent_events"] = TrackingEvent.objects.select_related("visitor_session")[:50]
        return context


def _event_detail(event):
    if event.event_type == "scroll_depth":
        return f"وصل إلى {event.metadata.get('depth', 0)}% من الصفحة"
    if event.event_type == "cta_click":
        return event.metadata.get("text") or event.metadata.get("href") or "ضغط على زر"
    if event.event_type == "map_interaction":
        return f"نوع التفاعل: {event.metadata.get('interaction', 'تفاعل')}"
    if event.duration_seconds:
        return f"المدة المسجلة: {event.duration_seconds} ثانية"
    return event.project_name or ""


class PermissionMenuItem(MenuItem):
    def __init__(self, *args, permission, **kwargs):
        self.permission = permission
        super().__init__(*args, **kwargs)

    def is_shown(self, request):
        return request.user.has_perm(self.permission)


@hooks.register("register_admin_urls")
def register_custom_admin_urls():
    return [
        path("leads/", LeadListView.as_view(), name="hig_leads_list"),
        path("leads/<int:pk>/", LeadDetailView.as_view(), name="hig_lead_detail"),
        path("tracking-summary/", TrackingSummaryView.as_view(), name="tracking_summary"),
    ]


@hooks.register("register_admin_menu_item")
def register_leads_menu_item():
    return PermissionMenuItem(
        "Leads",
        "/higadmin/leads/",
        icon_name="form",
        order=900,
        permission="leads.view_lead",
    )


@hooks.register("register_admin_menu_item")
def register_tracking_summary_menu_item():
    return PermissionMenuItem(
        "Tracking Summary",
        "/higadmin/tracking-summary/",
        icon_name="view",
        order=910,
        permission="tracking.view_trackingevent",
    )
