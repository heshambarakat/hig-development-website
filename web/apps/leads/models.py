import uuid

from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet

from apps.tracking.models import VisitorSession


@register_snippet
class Lead(models.Model):
    name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    project = models.CharField(max_length=160, blank=True)
    unit_type = models.CharField(max_length=120, blank=True)
    budget = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    language = models.CharField(max_length=10, blank=True)
    page_url = models.URLField(blank=True)
    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=160, blank=True)
    utm_content = models.CharField(max_length=160, blank=True)
    utm_term = models.CharField(max_length=160, blank=True)
    fbp = models.CharField(max_length=220, blank=True)
    fbc = models.CharField(max_length=220, blank=True)
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=80, default="new")
    notes = models.TextField(blank=True)
    google_sheet_synced = models.BooleanField(default=False)
    google_sheet_status = models.CharField(max_length=40, default="pending")
    google_sheet_error = models.TextField(blank=True)
    visitor_session = models.ForeignKey(
        VisitorSession,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="leads",
    )
    created_at = models.DateTimeField(default=timezone.now)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("phone"),
                FieldPanel("email"),
                FieldPanel("project"),
                FieldPanel("unit_type"),
                FieldPanel("budget"),
                FieldPanel("message"),
                FieldPanel("status"),
                FieldPanel("notes"),
            ],
            heading="Lead Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("language"),
                FieldPanel("page_url"),
                FieldPanel("utm_source"),
                FieldPanel("utm_medium"),
                FieldPanel("utm_campaign"),
                FieldPanel("utm_content"),
                FieldPanel("utm_term"),
                FieldPanel("fbp"),
                FieldPanel("fbc"),
                FieldPanel("visitor_session"),
            ],
            heading="Tracking",
        ),
        MultiFieldPanel(
            [
                FieldPanel("google_sheet_synced"),
                FieldPanel("google_sheet_status"),
                FieldPanel("google_sheet_error"),
            ],
            heading="Google Sheets",
        ),
    ]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.phone}"

    @property
    def journey_summary(self):
        if not self.visitor_session_id:
            return "No visitor session linked."
        events = self.visitor_session.events.order_by("occurred_at")
        return " -> ".join(events.values_list("event_type", flat=True)[:12])
