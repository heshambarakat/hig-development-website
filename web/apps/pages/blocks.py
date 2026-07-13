from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class BaseSectionBlock(blocks.StructBlock):
    show_section = blocks.BooleanBlock(required=False, default=True)
    layout_variant = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("default", "Default"),
            ("split", "Split"),
            ("centered", "Centered"),
            ("compact", "Compact"),
            ("feature", "Feature"),
        ],
        default="default",
    )
    background_color = blocks.CharBlock(required=False, max_length=40, help_text="CSS color, Tailwind token, or hex value.")
    text_color = blocks.CharBlock(required=False, max_length=40)
    animation_type = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("fade-up", "Fade up"),
            ("fade", "Fade"),
            ("none", "None"),
        ],
        default="fade-up",
    )
    section_anchor_id = blocks.CharBlock(required=False, max_length=80)

    class Meta:
        abstract = True


class ButtonMixin(blocks.StructBlock):
    button_text_ar = blocks.CharBlock(required=False, max_length=120)
    button_text_en = blocks.CharBlock(required=False, max_length=120)
    button_link = blocks.CharBlock(required=False, max_length=500)
    show_button = blocks.BooleanBlock(required=False, default=True)
    button_style = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("primary", "Primary"),
            ("secondary", "Secondary"),
            ("outline", "Outline"),
            ("ghost", "Ghost"),
        ],
        default="primary",
    )
    button_new_tab = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        abstract = True


class HeroBlock(BaseSectionBlock, ButtonMixin):
    eyebrow_ar = blocks.CharBlock(required=False, max_length=120)
    eyebrow_en = blocks.CharBlock(required=False, max_length=120)
    title_ar = blocks.CharBlock(required=False, max_length=220)
    title_en = blocks.CharBlock(required=False, max_length=220)
    subtitle_ar = blocks.TextBlock(required=False)
    subtitle_en = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)
    video_url = blocks.CharBlock(required=False, max_length=500, help_text="Local static/media path or full video URL.")

    class Meta:
        template = "blocks/hero_block.html"
        icon = "home"


class TextImageBlock(BaseSectionBlock, ButtonMixin):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    text_ar = blocks.RichTextBlock(required=False)
    text_en = blocks.RichTextBlock(required=False)
    image = ImageChooserBlock(required=False)
    secondary_image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/text_image_block.html"
        icon = "image"


class GalleryBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    images = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        template = "blocks/gallery_block.html"
        icon = "image"


class VideoBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    video_url = blocks.CharBlock(required=False, max_length=500, help_text="Local static/media path or full video URL.")
    poster = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/video_block.html"
        icon = "media"


class CTAButtonBlock(BaseSectionBlock, ButtonMixin):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    text_ar = blocks.TextBlock(required=False)
    text_en = blocks.TextBlock(required=False)

    class Meta:
        template = "blocks/cta_button_block.html"
        icon = "link"


class StatItemBlock(blocks.StructBlock):
    value = blocks.CharBlock(max_length=40)
    label_ar = blocks.CharBlock(max_length=120)
    label_en = blocks.CharBlock(required=False, max_length=120)


class StatsBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    stats = blocks.ListBlock(StatItemBlock())

    class Meta:
        template = "blocks/stats_block.html"
        icon = "plus"


class BoardMemberItemBlock(blocks.StructBlock):
    name_ar = blocks.CharBlock(max_length=140)
    name_en = blocks.CharBlock(max_length=140)
    title_ar = blocks.CharBlock(required=False, max_length=160)
    title_en = blocks.CharBlock(required=False, max_length=160)
    bio_ar = blocks.TextBlock(required=False)
    bio_en = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)


class BoardMembersBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180, default="مجلس الإدارة")
    title_en = blocks.CharBlock(required=False, max_length=180, default="Board Members")
    subtitle_ar = blocks.TextBlock(required=False)
    subtitle_en = blocks.TextBlock(required=False)
    members = blocks.ListBlock(BoardMemberItemBlock())

    class Meta:
        template = "blocks/board_members_block.html"
        icon = "group"


class LocationBlock(BaseSectionBlock, ButtonMixin):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    address_ar = blocks.TextBlock(required=False)
    address_en = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/location_block.html"
        icon = "site"


class NearbyPlaceBlock(blocks.StructBlock):
    name_ar = blocks.CharBlock(max_length=140)
    name_en = blocks.CharBlock(required=False, max_length=140)
    distance_ar = blocks.CharBlock(required=False, max_length=80)
    distance_en = blocks.CharBlock(required=False, max_length=80)


class DynamicMapBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    latitude = blocks.DecimalBlock(required=False, max_digits=10, decimal_places=7)
    longitude = blocks.DecimalBlock(required=False, max_digits=10, decimal_places=7)
    zoom_level = blocks.IntegerBlock(required=False, default=15, min_value=1, max_value=20)
    marker_title_ar = blocks.CharBlock(required=False, max_length=160)
    marker_title_en = blocks.CharBlock(required=False, max_length=160)
    marker_description_ar = blocks.TextBlock(required=False)
    marker_description_en = blocks.TextBlock(required=False)
    directions_url = blocks.URLBlock(required=False)
    nearby_places = blocks.ListBlock(NearbyPlaceBlock(), required=False)

    class Meta:
        template = "blocks/dynamic_map_block.html"
        icon = "site"


class NearbyPlacesBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    places = blocks.ListBlock(NearbyPlaceBlock())

    class Meta:
        template = "blocks/nearby_places_block.html"
        icon = "list-ul"


class SimpleItemBlock(blocks.StructBlock):
    title_ar = blocks.CharBlock(max_length=160)
    title_en = blocks.CharBlock(required=False, max_length=160)
    description_ar = blocks.TextBlock(required=False)
    description_en = blocks.TextBlock(required=False)


class FacilitiesBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    facilities = blocks.ListBlock(SimpleItemBlock())

    class Meta:
        template = "blocks/card_grid_block.html"
        icon = "tick"


class UnitTypesBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    unit_types = blocks.ListBlock(SimpleItemBlock())

    class Meta:
        template = "blocks/card_grid_block.html"
        icon = "table"


class PaymentPlansBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    plans = blocks.ListBlock(SimpleItemBlock())

    class Meta:
        template = "blocks/card_grid_block.html"
        icon = "form"


class FAQItemBlock(blocks.StructBlock):
    question_ar = blocks.CharBlock(max_length=220)
    question_en = blocks.CharBlock(required=False, max_length=220)
    answer_ar = blocks.RichTextBlock()
    answer_en = blocks.RichTextBlock(required=False)


class FAQBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    faqs = blocks.ListBlock(FAQItemBlock())

    class Meta:
        template = "blocks/faq_block.html"
        icon = "help"


class LeadFormBlock(BaseSectionBlock):
    title_ar = blocks.CharBlock(required=False, max_length=180)
    title_en = blocks.CharBlock(required=False, max_length=180)
    project_name = blocks.CharBlock(required=False, max_length=160)
    button_text_ar = blocks.CharBlock(required=False, max_length=80, default="اطلب تواصل")
    button_text_en = blocks.CharBlock(required=False, max_length=80, default="Request a Call")

    class Meta:
        template = "blocks/lead_form_block.html"
        icon = "form"


class ProjectBrandBlock(BaseSectionBlock):
    project_name_ar = blocks.CharBlock(required=False, max_length=180)
    project_name_en = blocks.CharBlock(required=False, max_length=180)
    logo = ImageChooserBlock(required=False)
    primary_color = blocks.CharBlock(required=False, max_length=40)
    secondary_color = blocks.CharBlock(required=False, max_length=40)
    description_ar = blocks.TextBlock(required=False)
    description_en = blocks.TextBlock(required=False)

    class Meta:
        template = "blocks/project_brand_block.html"
        icon = "site"


class SpacerBlock(blocks.StructBlock):
    size = blocks.ChoiceBlock(
        choices=[("sm", "Small"), ("md", "Medium"), ("lg", "Large")],
        default="md",
    )

    class Meta:
        template = "blocks/spacer_block.html"
        icon = "arrows-up-down"


CONTENT_BLOCKS = [
    ("hero", HeroBlock()),
    ("text_image", TextImageBlock()),
    ("gallery", GalleryBlock()),
    ("video", VideoBlock()),
    ("cta_button", CTAButtonBlock()),
    ("stats", StatsBlock()),
    ("board_members", BoardMembersBlock()),
    ("location", LocationBlock()),
    ("dynamic_map", DynamicMapBlock()),
    ("nearby_places", NearbyPlacesBlock()),
    ("facilities", FacilitiesBlock()),
    ("unit_types", UnitTypesBlock()),
    ("payment_plans", PaymentPlansBlock()),
    ("faq", FAQBlock()),
    ("lead_form", LeadFormBlock()),
    ("project_brand", ProjectBrandBlock()),
    ("spacer", SpacerBlock()),
]
