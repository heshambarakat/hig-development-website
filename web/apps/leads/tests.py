import json
import uuid
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

from apps.leads.models import Lead
from apps.tracking.models import TrackingEvent, VisitorSession


class LeadJourneyTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="review-admin", email="admin@example.com", password="test-password"
        )

    def test_tracking_event_and_lead_submission_share_session(self):
        browser_event_id = uuid.uuid4()
        tracked = self.client.post(
            "/tracking/event/",
            data=json.dumps(
                {
                    "event_type": "page_view",
                    "page_url": "http://testserver.local/ar/projects/barah-residence/",
                    "project_name": "BARAH Residence",
                    "utm_source": "facebook",
                    "utm_campaign": "barah-first-touch",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(tracked.status_code, 200)

        with patch("apps.leads.views.sync_lead_to_google_sheet"), patch(
            "apps.leads.views.send_meta_lead_event"
        ):
            response = self.client.post(
                "/leads/submit/",
                {
                    "name": "Test Lead",
                    "phone": "01144815252",
                    "project": "BARAH Residence",
                    "language": "ar",
                    "page_url": "http://testserver.local/ar/projects/barah-residence/",
                    "event_id": str(browser_event_id),
                },
            )

        self.assertRedirects(response, "/ar/thank-you/", fetch_redirect_response=False)
        lead = Lead.objects.get(name="Test Lead")
        self.assertIsNotNone(lead.visitor_session)
        self.assertEqual(lead.event_id, browser_event_id)
        self.assertEqual(lead.utm_source, "facebook")
        self.assertEqual(lead.utm_campaign, "barah-first-touch")
        self.assertTrue(
            TrackingEvent.objects.filter(
                visitor_session=lead.visitor_session, event_type="lead_submit"
            ).exists()
        )
        self.assertTrue(
            TrackingEvent.objects.filter(
                visitor_session=lead.visitor_session, event_type="page_view"
            ).exists()
        )

    def test_english_lead_redirects_to_english_thank_you(self):
        with patch("apps.leads.views.sync_lead_to_google_sheet"), patch(
            "apps.leads.views.send_meta_lead_event"
        ):
            response = self.client.post(
                "/leads/submit/",
                {"name": "English Lead", "phone": "201144815252", "language": "en"},
            )
        self.assertRedirects(response, "/en/thank-you/", fetch_redirect_response=False)

    def test_lead_dashboard_requires_admin_access_and_renders_journey(self):
        session = VisitorSession.objects.create(session_key="dashboard-session")
        event = TrackingEvent.objects.create(
            visitor_session=session,
            event_type="scroll_depth",
            page_url="http://testserver.local/ar/",
            metadata={"depth": 75},
        )
        lead = Lead.objects.create(
            name="Dashboard Lead", phone="01144815252", visitor_session=session
        )

        anonymous = self.client.get(f"/higadmin/leads/{lead.pk}/")
        self.assertEqual(anonymous.status_code, 302)

        self.client.force_login(self.admin)
        response = self.client.get(f"/higadmin/leads/{lead.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "رحلة العميل بالترتيب")
        self.assertContains(response, "75%")
        self.assertContains(response, event.page_url)

    def test_staff_without_lead_permission_cannot_open_dashboard(self):
        limited = get_user_model().objects.create_user(
            username="limited-editor", password="test-password", is_staff=True
        )
        limited.user_permissions.add(Permission.objects.get(codename="access_admin"))
        limited = get_user_model().objects.get(pk=limited.pk)
        self.assertTrue(limited.has_perm("wagtailadmin.access_admin"))
        self.assertFalse(limited.has_perm("leads.view_lead"))
        lead = Lead.objects.create(name="Private Lead", phone="01144815252")
        self.client.force_login(limited)
        response = self.client.get(f"/higadmin/leads/{lead.pk}/")
        self.assertIn(response.status_code, (302, 403))

    def test_tracking_rejects_invalid_or_oversized_metadata(self):
        invalid = self.client.post(
            "/tracking/event/",
            data=json.dumps({"event_type": "page_view", "metadata": []}),
            content_type="application/json",
        )
        self.assertEqual(invalid.status_code, 400)
        oversized = self.client.post(
            "/tracking/event/",
            data=json.dumps({"event_type": "page_view", "metadata": {"value": "x" * 5000}}),
            content_type="application/json",
        )
        self.assertEqual(oversized.status_code, 400)
