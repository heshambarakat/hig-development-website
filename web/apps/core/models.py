from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import PreviewableMixin
from wagtail.snippets.models import register_snippet


@register_snippet
class NewWebContent(PreviewableMixin, models.Model):
    title = models.CharField(max_length=120, default="HIG New Website Content")

    hero_text_ar = models.TextField(blank=True)
    hero_text_en = models.TextField(blank=True)
    hero_title_ar = models.CharField(max_length=180, blank=True, default="WE KNOW THE ROUTE.")
    hero_title_en = models.CharField(max_length=180, blank=True, default="WE KNOW THE ROUTE.")
    hero_video = models.FileField(upload_to="newweb/videos/", blank=True)
    hero_poster = models.ImageField(upload_to="newweb/images/", blank=True)
    show_hero = models.BooleanField(default=True)

    who_title_ar = models.CharField(max_length=220, blank=True)
    who_title_en = models.CharField(max_length=220, blank=True)
    who_text_ar = models.TextField(blank=True)
    who_text_en = models.TextField(blank=True)

    value_1_title_ar = models.CharField(max_length=120, blank=True)
    value_1_title_en = models.CharField(max_length=120, blank=True)
    value_1_text_ar = models.TextField(blank=True)
    value_1_text_en = models.TextField(blank=True)
    value_2_title_ar = models.CharField(max_length=120, blank=True)
    value_2_title_en = models.CharField(max_length=120, blank=True)
    value_2_text_ar = models.TextField(blank=True)
    value_2_text_en = models.TextField(blank=True)
    value_3_title_ar = models.CharField(max_length=120, blank=True)
    value_3_title_en = models.CharField(max_length=120, blank=True)
    value_3_text_ar = models.TextField(blank=True)
    value_3_text_en = models.TextField(blank=True)
    value_4_title_ar = models.CharField(max_length=120, blank=True)
    value_4_title_en = models.CharField(max_length=120, blank=True)
    value_4_text_ar = models.TextField(blank=True)
    value_4_text_en = models.TextField(blank=True)

    barah_tagline_ar = models.CharField(max_length=160, blank=True)
    barah_tagline_en = models.CharField(max_length=160, blank=True)
    barah_text_ar = models.TextField(blank=True)
    barah_text_en = models.TextField(blank=True)
    caza_text_ar = models.TextField(blank=True)
    caza_text_en = models.TextField(blank=True)
    centro_text_ar = models.TextField(blank=True)
    centro_text_en = models.TextField(blank=True)
    parco_text_ar = models.TextField(blank=True)
    parco_text_en = models.TextField(blank=True)
    featured_title_ar = models.CharField(max_length=220, blank=True)
    featured_title_en = models.CharField(max_length=220, blank=True)

    team_title_ar = models.CharField(max_length=180, blank=True)
    team_title_en = models.CharField(max_length=180, blank=True)
    team_text_ar = models.TextField(blank=True)
    team_text_en = models.TextField(blank=True)

    insights_title_ar = models.CharField(max_length=180, blank=True)
    insights_title_en = models.CharField(max_length=180, blank=True)
    insight_1_ar = models.CharField(max_length=220, blank=True)
    insight_1_en = models.CharField(max_length=220, blank=True)
    insight_2_ar = models.CharField(max_length=220, blank=True)
    insight_2_en = models.CharField(max_length=220, blank=True)
    insight_3_ar = models.CharField(max_length=220, blank=True)
    insight_3_en = models.CharField(max_length=220, blank=True)

    contact_title_ar = models.CharField(max_length=180, blank=True)
    contact_title_en = models.CharField(max_length=180, blank=True)
    contact_text_ar = models.TextField(blank=True)
    contact_text_en = models.TextField(blank=True)

    # Global identity and layout controls. Values become CSS custom properties,
    # keeping editor choices centralized and responsive rules intact.
    primary_color = models.CharField(max_length=20, default="#1279d7")
    dark_color = models.CharField(max_length=20, default="#05070a")
    light_color = models.CharField(max_length=20, default="#f4f8fd")
    body_font_size = models.PositiveSmallIntegerField(default=16)
    navigation_font_size = models.PositiveSmallIntegerField(default=13)
    hero_title_size = models.PositiveSmallIntegerField(default=180)
    section_title_size = models.PositiveSmallIntegerField(default=88)
    project_title_size = models.PositiveSmallIntegerField(default=96)
    body_line_height = models.DecimalField(max_digits=3, decimal_places=2, default=1.80)
    arabic_title_line_height = models.DecimalField(max_digits=3, decimal_places=2, default=1.34)
    section_spacing = models.PositiveSmallIntegerField(default=112)
    content_max_width = models.PositiveSmallIntegerField(default=1920)
    header_height = models.PositiveSmallIntegerField(default=92)
    logo_width = models.PositiveSmallIntegerField(default=112)
    hero_min_height = models.PositiveSmallIntegerField(default=100)
    card_radius = models.PositiveSmallIntegerField(default=4)
    form_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.20)

    show_header = models.BooleanField(default=True)
    show_stats = models.BooleanField(default=True)
    show_featured_project = models.BooleanField(default=True)
    show_project_lanes = models.BooleanField(default=True)
    show_projects_grid = models.BooleanField(default=True)
    show_board = models.BooleanField(default=True)
    show_insights = models.BooleanField(default=True)
    show_contact = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)
    show_whatsapp = models.BooleanField(default=True)

    hotline = models.CharField(max_length=30, default="17556")
    whatsapp_number = models.CharField(max_length=30, default="201144815252")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    footer_text_ar = models.TextField(blank=True)
    footer_text_en = models.TextField(blank=True)

    panels = [
        FieldPanel("title"),
        MultiFieldPanel(
            [
                FieldPanel("show_hero"),
                FieldPanel("hero_title_ar"),
                FieldPanel("hero_title_en"),
                FieldPanel("hero_text_ar"),
                FieldPanel("hero_text_en"),
                FieldPanel("hero_video"),
                FieldPanel("hero_poster"),
            ],
            heading="Hero",
            help_text="تحكم في عنوان ونص وفيديو وصورة أول شاشة في الصفحة الرئيسية. أوقف Show hero لإخفاء القسم بالكامل.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("who_title_ar"),
                FieldPanel("who_title_en"),
                FieldPanel("who_text_ar"),
                FieldPanel("who_text_en"),
            ],
            heading="Who We Are",
            help_text="النصوص التي تظهر في قسم من نحن بعد الهيرو مباشرة، بالعربية والإنجليزية.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("value_1_title_ar"),
                FieldPanel("value_1_title_en"),
                FieldPanel("value_1_text_ar"),
                FieldPanel("value_1_text_en"),
                FieldPanel("value_2_title_ar"),
                FieldPanel("value_2_title_en"),
                FieldPanel("value_2_text_ar"),
                FieldPanel("value_2_text_en"),
                FieldPanel("value_3_title_ar"),
                FieldPanel("value_3_title_en"),
                FieldPanel("value_3_text_ar"),
                FieldPanel("value_3_text_en"),
                FieldPanel("value_4_title_ar"),
                FieldPanel("value_4_title_en"),
                FieldPanel("value_4_text_ar"),
                FieldPanel("value_4_text_en"),
            ],
            heading="Values",
            help_text="محتوى قيم الشركة. هذه الحقول محفوظة للتوسع ويمكن تعديل نصوص اللغتين من هنا.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("barah_tagline_ar"),
                FieldPanel("barah_tagline_en"),
                FieldPanel("barah_text_ar"),
                FieldPanel("barah_text_en"),
                FieldPanel("caza_text_ar"),
                FieldPanel("caza_text_en"),
                FieldPanel("centro_text_ar"),
                FieldPanel("centro_text_en"),
                FieldPanel("parco_text_ar"),
                FieldPanel("parco_text_en"),
                FieldPanel("featured_title_ar"),
                FieldPanel("featured_title_en"),
            ],
            heading="Projects",
            help_text="عناوين ووصف BARAH والمشروعات التجارية وقسم المشروعات المختارة في الصفحة الرئيسية.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("team_title_ar"),
                FieldPanel("team_title_en"),
                FieldPanel("team_text_ar"),
                FieldPanel("team_text_en"),
            ],
            heading="Board Members",
            help_text="عنوان ووصف قسم مجلس الإدارة الظاهر في الصفحة الرئيسية.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("insights_title_ar"),
                FieldPanel("insights_title_en"),
                FieldPanel("insight_1_ar"),
                FieldPanel("insight_1_en"),
                FieldPanel("insight_2_ar"),
                FieldPanel("insight_2_en"),
                FieldPanel("insight_3_ar"),
                FieldPanel("insight_3_en"),
            ],
            heading="Insights",
            help_text="عنوان قسم الأخبار وأسماء المقالات الثلاثة الظاهرة في الصفحة الرئيسية.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_title_ar"),
                FieldPanel("contact_title_en"),
                FieldPanel("contact_text_ar"),
                FieldPanel("contact_text_en"),
            ],
            heading="Contact",
            help_text="عنوان ووصف قسم التسجيل الموجود قبل الفوتر.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("primary_color"), FieldPanel("dark_color"), FieldPanel("light_color"),
                FieldPanel("body_font_size"), FieldPanel("navigation_font_size"),
                FieldPanel("hero_title_size"), FieldPanel("section_title_size"),
                FieldPanel("project_title_size"), FieldPanel("body_line_height"),
                FieldPanel("arabic_title_line_height"), FieldPanel("section_spacing"),
                FieldPanel("content_max_width"), FieldPanel("header_height"),
                FieldPanel("logo_width"), FieldPanel("hero_min_height"),
                FieldPanel("card_radius"), FieldPanel("form_opacity"),
            ],
            heading="Design controls",
            help_text="إعدادات التصميم العامة: الألوان، أحجام الخطوط، ارتفاع السطور، المسافات، ارتفاع الهيدر والهيرو، حجم اللوجو، استدارة الكروت ووضوح الفورم. القيم الرقمية بالبكسل ما عدا Hero min height فهي نسبة من ارتفاع الشاشة.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("show_header"), FieldPanel("show_stats"),
                FieldPanel("show_featured_project"), FieldPanel("show_project_lanes"),
                FieldPanel("show_projects_grid"), FieldPanel("show_board"),
                FieldPanel("show_insights"), FieldPanel("show_contact"),
                FieldPanel("show_footer"), FieldPanel("show_whatsapp"),
            ],
            heading="Section visibility",
            help_text="كل اختيار يتحكم في ظهور أو إخفاء القسم المقابل في الصفحة الرئيسية، بدون حذف محتواه.",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hotline"), FieldPanel("whatsapp_number"),
                FieldPanel("facebook_url"), FieldPanel("instagram_url"),
                FieldPanel("youtube_url"), FieldPanel("linkedin_url"),
                FieldPanel("footer_text_ar"), FieldPanel("footer_text_en"),
            ],
            heading="Header, social links and footer",
            help_text="رقم الخط الساخن وواتساب وروابط السوشيال ونص الفوتر باللغتين. اكتب رابط السوشيال كاملًا شامل https://.",
        ),
    ]

    class Meta:
        verbose_name = "New Website Content"
        verbose_name_plural = "New Website Content"

    def __str__(self):
        return self.title

    @property
    def preview_modes(self):
        return [("ar", "معاينة عربية"), ("en", "English preview")]

    @property
    def default_preview_mode(self):
        return "ar"

    def get_full_url(self):
        return "/ar/"

    def get_preview_template(self, request, mode_name):
        return "newweb/index.html"

    def get_preview_context(self, request, mode_name):
        from apps.core.views import build_newweb_context

        return build_newweb_context(mode_name or "ar", self, request=request)
