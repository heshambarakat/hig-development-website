from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string


class SEOMixin(models.Model):
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True)
    og_title = models.CharField(max_length=160, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    json_ld_schema = models.JSONField(blank=True, null=True)

    seo_panels = [
        MultiFieldPanel(
            [
                FieldPanel("meta_title"),
                FieldPanel("meta_description"),
                FieldPanel("canonical_url"),
                FieldPanel("og_title"),
                FieldPanel("og_description"),
                FieldPanel("og_image"),
                FieldPanel("json_ld_schema"),
            ],
            heading="SEO / AEO",
        )
    ]

    class Meta:
        abstract = True
