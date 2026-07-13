from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page

from apps.pages.blocks import CONTENT_BLOCKS
from apps.seo.models import SEOMixin


class ProjectsIndexPage(SEOMixin, Page):
    template = "projects/projects_index_page.html"
    parent_page_types = ["pages.HomePage"]
    subpage_types = ["projects.ProjectDetailPage"]
    intro_ar = models.TextField(blank=True)
    intro_en = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro_ar"),
        FieldPanel("intro_en"),
    ]
    promote_panels = Page.promote_panels + SEOMixin.seo_panels

    def get_context(self, request):
        context = super().get_context(request)
        context["projects"] = ProjectDetailPage.objects.live().descendant_of(self).order_by("title")
        return context


class ProjectDetailPage(SEOMixin, Page):
    template = "projects/project_detail_page.html"
    parent_page_types = ["projects.ProjectsIndexPage"]
    subpage_types = ["pages.LandingPage", "pages.ThankYouPage"]

    project_name_ar = models.CharField(max_length=180, blank=True)
    project_name_en = models.CharField(max_length=180, blank=True)
    brand_primary_color = models.CharField(max_length=40, blank=True)
    brand_secondary_color = models.CharField(max_length=40, blank=True)
    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_video_url = models.CharField(max_length=500, blank=True)

    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    map_zoom = models.PositiveSmallIntegerField(default=15)
    map_marker_title = models.CharField(max_length=160, blank=True)
    map_marker_description = models.TextField(blank=True)
    project_address = models.TextField(blank=True)
    directions_url = models.URLField(blank=True)
    nearby_landmarks = models.JSONField(default=list, blank=True, help_text="List of landmarks with name/distance fields.")
    show_map = models.BooleanField(default=True)

    body = StreamField(CONTENT_BLOCKS, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("project_name_ar"),
                FieldPanel("project_name_en"),
                FieldPanel("brand_primary_color"),
                FieldPanel("brand_secondary_color"),
                FieldPanel("logo"),
                FieldPanel("hero_image"),
                FieldPanel("hero_video_url"),
            ],
            heading="Project Brand",
        ),
        MultiFieldPanel(
            [
                FieldPanel("show_map"),
                FieldPanel("latitude"),
                FieldPanel("longitude"),
                FieldPanel("map_zoom"),
                FieldPanel("map_marker_title"),
                FieldPanel("map_marker_description"),
                FieldPanel("project_address"),
                FieldPanel("directions_url"),
                FieldPanel("nearby_landmarks"),
            ],
            heading="Dynamic Map",
        ),
        FieldPanel("body"),
    ]
    promote_panels = Page.promote_panels + SEOMixin.seo_panels
