from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from apps.core.models import NewWebContent


class PrimaryWebsiteTests(TestCase):
    def test_root_redirects_to_arabic_primary_home(self):
        response = self.client.get("/")
        self.assertRedirects(response, "/ar/", fetch_redirect_response=False)

    def test_arabic_and_english_primary_routes_render_new_design(self):
        for path, language in (("/ar/", "ar"), ("/en/", "en")):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'class="nw-page"')
            self.assertContains(response, f'lang="{language}"')

    def test_editor_design_controls_are_rendered_as_css_variables(self):
        NewWebContent.objects.create(
            title="Website settings",
            primary_color="#0057b8",
            hero_title_size=144,
            logo_width=128,
        )
        response = self.client.get("/ar/")
        self.assertContains(response, "--blue: #0057b8")
        self.assertContains(response, "--hero-title-size: 144px")
        self.assertContains(response, "--logo-width: 128px")

    def test_sections_can_be_hidden_from_admin_controls(self):
        NewWebContent.objects.create(title="Website settings", show_board=False)
        response = self.client.get("/en/")
        self.assertNotContains(response, 'class="nw-board nw-section"')

    def test_editor_has_arabic_and_english_live_preview_modes(self):
        content = NewWebContent.objects.create(
            title="Website settings",
            hero_title_ar="عنوان المعاينة",
            hero_title_en="Preview title",
        )
        self.assertEqual(content.preview_modes[0][0], "ar")
        self.assertEqual(content.preview_modes[1][0], "en")
        context = content.get_preview_context(RequestFactory().get("/ar/"), "ar")
        self.assertEqual(context["t"]["hero_title"], "عنوان المعاينة")
        self.assertIs(context["site_controls"], content)
