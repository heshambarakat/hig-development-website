from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from apps.pages.blocks import CONTENT_BLOCKS
from apps.seo.models import SEOMixin


class FlexiblePageMixin(SEOMixin, models.Model):
    body = StreamField(CONTENT_BLOCKS, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [FieldPanel("body")]

    class Meta:
        abstract = True


class HomePage(FlexiblePageMixin, Page):
    template = "pages/home_page.html"
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "pages.AboutPage",
        "projects.ProjectsIndexPage",
        "pages.NewsIndexPage",
        "pages.ContactPage",
        "pages.LandingPage",
        "pages.ThankYouPage",
    ]

    content_panels = FlexiblePageMixin.content_panels
    promote_panels = Page.promote_panels + SEOMixin.seo_panels

    def get_context(self, request):
        context = super().get_context(request)
        from apps.projects.models import ProjectDetailPage

        context["featured_projects"] = ProjectDetailPage.objects.live().order_by("title")
        context["latest_articles"] = NewsArticlePage.objects.live().order_by("-first_published_at")[:3]
        context["show_preloader"] = True
        context["show_home_language_switch"] = True
        return context


class AboutPage(FlexiblePageMixin, Page):
    template = "pages/flexible_page.html"
    parent_page_types = ["pages.HomePage"]
    subpage_types = []
    content_panels = FlexiblePageMixin.content_panels
    promote_panels = Page.promote_panels + SEOMixin.seo_panels


class NewsIndexPage(FlexiblePageMixin, Page):
    template = "pages/news_index_page.html"
    parent_page_types = ["pages.HomePage"]
    subpage_types = ["pages.NewsArticlePage"]
    content_panels = FlexiblePageMixin.content_panels
    promote_panels = Page.promote_panels + SEOMixin.seo_panels

    def get_context(self, request):
        context = super().get_context(request)
        context["articles"] = NewsArticlePage.objects.live().descendant_of(self).order_by("-first_published_at")
        return context


class NewsArticlePage(FlexiblePageMixin, Page):
    template = "pages/news_article_page.html"
    parent_page_types = ["pages.NewsIndexPage"]
    subpage_types = []
    intro = models.TextField(blank=True)
    title_ar = models.CharField(max_length=220, blank=True)
    title_en = models.CharField(max_length=220, blank=True)
    intro_ar = models.TextField(blank=True)
    intro_en = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("title_ar"),
        FieldPanel("title_en"),
        FieldPanel("intro"),
        FieldPanel("intro_ar"),
        FieldPanel("intro_en"),
        FieldPanel("date"),
        FieldPanel("body"),
    ]
    promote_panels = Page.promote_panels + SEOMixin.seo_panels


class ContactPage(FlexiblePageMixin, Page):
    template = "pages/contact_page.html"
    parent_page_types = ["pages.HomePage"]
    subpage_types = []
    content_panels = FlexiblePageMixin.content_panels
    promote_panels = Page.promote_panels + SEOMixin.seo_panels


class LandingPage(FlexiblePageMixin, Page):
    template = "pages/landing_page.html"
    parent_page_types = ["pages.HomePage", "projects.ProjectDetailPage"]
    subpage_types = ["pages.ThankYouPage"]
    content_panels = FlexiblePageMixin.content_panels
    promote_panels = Page.promote_panels + SEOMixin.seo_panels


class ThankYouPage(FlexiblePageMixin, Page):
    template = "pages/thank_you_page.html"
    parent_page_types = ["pages.HomePage", "pages.LandingPage", "projects.ProjectDetailPage"]
    subpage_types = []
    content_panels = FlexiblePageMixin.content_panels
    promote_panels = Page.promote_panels + SEOMixin.seo_panels
