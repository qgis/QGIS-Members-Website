# coding=utf-8
# flake8: noqa

from unittest.mock import patch
from unittest import mock
from django.urls import reverse
from django.test import TestCase, override_settings
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from base.tests.model_factories import ProjectF
from changes.tests.model_factories import (
    SponsorF,
)
from helpers.notification import send_notification
from core.model_factories import UserF
import logging


def mocked_send_notification(*args, **kwargs):
    return 'Mock document'


class TestSustainingMemberUpdateView(TestCase):
    """Tests that Sponsor views work."""

    @override_settings(VALID_DOMAIN=['testserver', ])
    def setUp(self):
        """
        Setup before each test
        We force the locale to en otherwise it will use
        the locale of the host running the tests and we
        will get unpredictable results / 404s
        """

        self.client = Client()
        self.client.post(
                '/set_language/', data={'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.project = ProjectF.create()
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.user2 = UserF.create(**{
            'username': 'user',
            'password': 'password',
            'is_staff': False
        })
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()
        self.user2.set_password('password')
        self.user2.save()

        self.sustaining_member = SponsorF.create(
            project=self.project,
            active=True,
            sustaining_membership=True,
            author=self.user2
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SustainingMemberUpdateView_get(self):
        """
        Test if user can open a sustaining member update view
        """
        self.client.login(username='user', password='password')

        response = self.client.get(reverse('sustaining-member-update', kwargs={
            'member_id': self.sustaining_member.id
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['is_sustaining_member'], True)
        expected_template = [
            'sustaining_member/update.html'
        ]
        self.assertEqual(response.template_name, expected_template)
        self.assertEqual(response.context['the_project'].slug,
                         self.project.slug)

    @override_settings(VALID_DOMAIN=['testserver', ])
    @patch(
        'changes.views.sustaining_member.send_notification')
    def test_SustainingMemberUpdateView_post(self, mock_send_notification):
        """
        Test if user can update a sustaining member
        """
        testfile = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b')
        logo = SimpleUploadedFile('small.jpeg', testfile,
                                  content_type='image/jpeg')

        self.client.login(username='user', password='password')

        post_data = {
            'name': 'test sustaining member',
            'logo': logo,
            'country': 'US',
        }
        response = self.client.post(reverse('sustaining-member-update', kwargs={
            'member_id': self.sustaining_member.id
        }), post_data)
        self.assertEqual(response.url,
                         reverse('sustaining-membership'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('sustaining-membership'))
        self.assertEqual(response.context['is_sustaining_member'], True)
        self.assertTrue(mock_send_notification.called)
