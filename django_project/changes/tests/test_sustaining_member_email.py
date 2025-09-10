import logging
from unittest.mock import patch

from changes.tests.model_factories import SponsorEmailF, SponsorshipLevelF
from core.model_factories import UserF
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

User = get_user_model()


@override_settings(VALID_DOMAIN=["testserver"])
class SponsorEmailViewsTest(TestCase):
    def setUp(self):
        """
        Setup before each test
        We force the locale to en otherwise it will use
        the locale of the host running the tests and we
        will get unpredictable results / 404s
        """

        self.client = Client()
        self.client.post("/set_language/", data={"language": "en"})
        logging.disable(logging.CRITICAL)
        # self.project = ProjectF.create()

        self.staff_user = UserF.create(username="staff", is_staff=True)
        self.staff_user.set_password("password")
        self.staff_user.save()
        self.client.login(username="staff", password="password")
        self.sponsor_email = SponsorEmailF.create(is_deleted=False)

    def test_list_view(self):
        url = reverse("sponsor-email-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("sponsoremails", response.context)
        self.assertTemplateUsed(response, "sponsor_email/list.html")

    def test_detail_view(self):
        url = reverse("sponsor-email-detail", kwargs={"pk": self.sponsor_email.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["sponsor_email"], self.sponsor_email)
        self.assertTemplateUsed(response, "sponsor_email/details.html")

    def test_create_view_get(self):
        url = reverse("sponsor-email-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sponsor_email/create.html")

    @patch("changes.models.sponsor_email.SponsorEmail.send_email")
    @patch("changes.models.sponsor_email.SponsorEmail.get_all_recipients")
    def test_create_view_post_with_recipients(
        self, mock_get_recipients, mock_send_email
    ):
        mock_get_recipients.return_value = {"to": ["test@example.com"]}
        url = reverse("sponsor-email-create")
        level = SponsorshipLevelF.create()
        data = {
            "subject": "Test Subject",
            "body": "Test Body",
            "email_type": "both",
            "cc": "cc@example.com",
            "status": "draft",
            "sponsor_levels": [level.pk],  # ManyToMany expects a list of IDs
        }
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse("sponsor-email-list"))
        mock_send_email.assert_called_once()

    @patch("changes.models.sponsor_email.SponsorEmail.send_email")
    @patch("changes.models.sponsor_email.SponsorEmail.get_all_recipients")
    def test_create_view_post_no_recipients(self, mock_get_recipients, mock_send_email):
        mock_get_recipients.return_value = {"to": []}
        url = reverse("sponsor-email-create")
        level = SponsorshipLevelF.create()
        data = {
            "subject": "Test Subject",
            "body": "Test Body",
            "email_type": "both",
            "cc": "cc@example.com",
            "status": "draft",
            "sponsor_levels": [level.pk],
        }
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse("sponsor-email-list"))
        mock_send_email.assert_not_called()
        messages = list(response.context["messages"])
        self.assertTrue(any("No recipients found" in str(m) for m in messages))

    def test_resend_view_get(self):
        url = reverse("sponsor-email-resend", kwargs={"pk": self.sponsor_email.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sponsor_email/resend.html")
        self.assertEqual(response.context["sponsor_email"], self.sponsor_email)

    @patch("changes.models.sponsor_email.SponsorEmail.send_email")
    @patch("changes.models.sponsor_email.SponsorEmail.get_all_recipients")
    def test_resend_view_post_with_recipients(
        self, mock_get_recipients, mock_send_email
    ):
        mock_get_recipients.return_value = {"to": ["test@example.com"]}
        url = reverse("sponsor-email-resend", kwargs={"pk": self.sponsor_email.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(
            response,
            reverse("sponsor-email-detail", kwargs={"pk": self.sponsor_email.pk}),
        )
        mock_send_email.assert_called_once()

    @patch("changes.models.sponsor_email.SponsorEmail.send_email")
    @patch("changes.models.sponsor_email.SponsorEmail.get_all_recipients")
    def test_resend_view_post_no_recipients(self, mock_get_recipients, mock_send_email):
        mock_get_recipients.return_value = {"to": []}
        url = reverse("sponsor-email-resend", kwargs={"pk": self.sponsor_email.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(
            response,
            reverse("sponsor-email-detail", kwargs={"pk": self.sponsor_email.pk}),
        )
        mock_send_email.assert_not_called()
        messages = list(response.context["messages"])
        self.assertTrue(any("No recipients found" in str(m) for m in messages))

    def test_delete_view_get(self):
        url = reverse("sponsor-email-delete", kwargs={"pk": self.sponsor_email.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sponsor_email/delete.html")
        self.assertEqual(response.context["sponsor_email"], self.sponsor_email)

    def test_delete_view_post(self):
        url = reverse("sponsor-email-delete", kwargs={"pk": self.sponsor_email.pk})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse("sponsor-email-list"))
        # Refresh from db and check is_deleted is True
        self.sponsor_email.refresh_from_db()
        self.assertTrue(self.sponsor_email.is_deleted)
