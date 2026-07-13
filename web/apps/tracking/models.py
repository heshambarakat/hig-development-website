import uuid

from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class VisitorSession(models.Model):
    visitor_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    session_key = models.CharField(max_length=80, unique=True, default=uuid.uuid4)
    first_landing_page = models.URLField(blank=True)
    last_page_url = models.URLField(blank=True)
    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=160, blank=True)
    utm_content = models.CharField(max_length=160, blank=True)
    utm_term = models.CharField(max_length=160, blank=True)
    device_browser = models.CharField(max_length=220, blank=True)
    marketing_consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("session_key"),
        FieldPanel("first_landing_page"),
        FieldPanel("last_page_url"),
        FieldPanel("utm_source"),
        FieldPanel("utm_medium"),
        FieldPanel("utm_campaign"),
        FieldPanel("utm_content"),
        FieldPanel("utm_term"),
        FieldPanel("device_browser"),
        FieldPanel("marketing_consent"),
    ]

    def __str__(self):
        return str(self.session_key)


@register_snippet
class TrackingEvent(models.Model):
    EVENT_TYPES = [
        ("session_started", "Session started"),
        ("page_view", "Page view"),
        ("project_view", "Project view"),
        ("map_interaction", "Map interaction"),
        ("scroll_depth", "Scroll depth"),
        ("cta_click", "CTA click"),
        ("lead_form_start", "Lead form start"),
        ("lead_submit", "Lead submit"),
    ]

    visitor_session = models.ForeignKey(
        VisitorSession,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events",
    )
    event_type = models.CharField(max_length=40, choices=EVENT_TYPES)
    page_url = models.URLField(blank=True)
    project_name = models.CharField(max_length=160, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    occurred_at = models.DateTimeField(default=timezone.now)

    panels = [
        FieldPanel("visitor_session"),
        FieldPanel("event_type"),
        FieldPanel("page_url"),
        FieldPanel("project_name"),
        FieldPanel("metadata"),
        FieldPanel("duration_seconds"),
        FieldPanel("occurred_at"),
    ]

    class Meta:
        ordering = ["-occurred_at"]

    def __str__(self):
        return f"{self.event_type} - {self.occurred_at:%Y-%m-%d %H:%M}"
