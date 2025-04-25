# coding=utf-8
# flake8: noqa

import datetime
import json
from datetime import timedelta
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.test.client import Client
from base.tests.model_factories import ProjectF
from changes.tests.model_factories import (
    SponsorshipLevelF,
    SponsorF,
    SponsorshipPeriodF)
from core.model_factories import UserF
import logging


class TestSponsorshipLevelViews(TestCase):
    """
    Tests that SponsorshipLevel views work.
    """

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
        self.sponsorship_level = SponsorshipLevelF.create(project=self.project)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.sponsorship_level.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelListView(self):

        response = self.client.get(reverse('sponsorshiplevel-list'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_level/list.html',
            u'changes/sponsorshiplevel_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)
        self.assertEqual(response.context_data['object_list'][0],
                         self.sponsorship_level)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsorshiplevel-create'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_level/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelCreateView_no_login(self):

        response = self.client.get(reverse('sponsorshiplevel-create'))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Sponsorship Level',
            'project': self.project.id,
            'sort_number': 0
        }
        response = self.client.post(reverse('sponsorshiplevel-create'), post_data)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelCreate_no_login(self):

        post_data = {
            'name': u'New Test Sponsorship Level'
        }
        response = self.client.post(reverse('sponsorshiplevel-create'), post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelDetailView(self):

        response = self.client.get(reverse('sponsorshiplevel-detail', kwargs={
            'slug': self.sponsorship_level.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_level/detail.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsorshiplevel-delete', kwargs={
            'slug': self.sponsorship_level.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_level/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelDeleteView_no_login(self):

        response = self.client.get(reverse('sponsorshiplevel-delete', kwargs={
            'slug': self.sponsorship_level.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelDelete_with_login(self):

        sponsorship_level_to_delete = SponsorshipLevelF.create(
                project=self.project)
        self.client.login(username='timlinux', password='password')
        response = self.client.post(reverse('sponsorshiplevel-delete', kwargs={
            'slug': sponsorship_level_to_delete.slug
        }), {})
        self.assertRedirects(
            response, reverse('sponsorshiplevel-list'))

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipLevelDelete_no_login(self):

        sponsorshiplevel_to_delete = SponsorshipLevelF.create(
            project=self.project
        )
        response = self.client.post(reverse('sponsorshiplevel-delete', kwargs={
            'slug': sponsorshiplevel_to_delete.slug
        }))
        self.assertEqual(response.status_code, 302)


class TestSponsorViews(TestCase):
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
        self.sponsor = SponsorF.create(project=self.project)
        self.current_sponsor = SponsorF.create(project=self.project)
        self.future_sponsor = SponsorF.create(project=self.project)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

        self.non_staff_user = UserF.create(**{
            'username': 'non-staff',
            'password': 'password',
            'is_staff': False
        })
        self.non_staff_user.set_password('password')
        self.non_staff_user.save()

        self.sponsorship_level = SponsorshipLevelF.create(
            project=self.project,
            name='Gold')
        self.today = datetime.date.today()
        self.past_sponsorship_period = SponsorshipPeriodF.create(
            project=self.project,
            sponsor=self.sponsor,
            sponsorship_level=self.sponsorship_level,
            start_date=self.today - timedelta(days=200),
            end_date=self.today - timedelta(days=100),
            approved=True)
        self.current_sponsorship_period = SponsorshipPeriodF.create(
            project=self.project,
            sponsor=self.current_sponsor,
            sponsorship_level=self.sponsorship_level,
            start_date=self.today,
            end_date=self.today + timedelta(days=700),
            approved=True)
        self.future_sponsorship_period = SponsorshipPeriodF.create(
            project=self.project,
            sponsor=self.future_sponsor,
            sponsorship_level=self.sponsorship_level,
            start_date=self.today + timedelta(days=200),
            end_date=self.today + timedelta(days=700),
            approved=True)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.sponsor.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorListView(self):

        response = self.client.get(reverse('sponsor-list'))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_FutureSponsorListView_no_login(self):
        response = self.client.get(reverse('future-sponsor-list'))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_FutureSponsorListView_with_staff_login(self):
        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('future-sponsor-list'))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_FutureSponsorListView_with_non_staff_login(self):
        self.client.login(username='non-staff', password='password')
        response = self.client.get(reverse('future-sponsor-list'))
        self.assertEqual(response.status_code, 404)


    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsor-create'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsor/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorCreateView_no_login(self):

        response = self.client.get(reverse('sponsor-create'))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Sponsor',
            'project': self.project.id,
            'sort_number': 0
        }
        response = self.client.post(reverse('sponsor-create'), post_data)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorCreate_no_login(self):

        post_data = {
            'name': u'New Test Sponsor'
        }
        response = self.client.post(reverse('sponsor-create'), post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorCreate_with_svg_logo(self):
        svg = ('<?xml version="1.0" standalone="no"?>'
               '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"'
               '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">'
               '<svg version="1.0" xmlns="http://www.w3.org/2000/svg"'
               'width="32.000000pt" height="32.000000pt" viewBox="0 0 '
               '32.000000 32.000000"'
               'preserveAspectRatio="xMidYMid meet"' >
               ''
               '<g transform="translate(0.000000,32.000000) '
               'scale(0.100000,-0.100000)"'
               'fill="#000000" stroke="none">'
               '<path d="M95 291 c-41 -18 -77 -68 -82 -113 -10 '
               '-99 84 -178 183 -154 25 7 26'
               '8 9 26 -11 12 -31 20 -50 20 -47 0 -85 41 -85 92 '
               '0 51 43 98 90 98 44 0 90'
               '-47 90 -93 0 -34 33 -78 48 -63 4 4 7 32 7 62 0 49'
               ' -3 57 -37 91 -33 33 -43'
               '37 -95 40 -32 1 -67 -1 -78 -6z"/>'
               '<path d="M140 156 c0 -13 7 -29 15 -36 13 -10 15 -9 '
               '15 9 0 13 6 21 16 21 14'
               '0 14 3 4 15 -20 24 -50 19 -50 -9z"/>'
               '<path d="M190 107 c0 -32 59 -87 93 -87 39 0 35 25 -12 '
               '71 -44 45 -81 52 -81'
               '16z"/>'
               '</g>'
               '</svg>')
        logo = SimpleUploadedFile('qgis.svg', svg)
        self.client.login(username='timlinux', password='password')
        post_data = {
            'name': u'New Test Sponsor',
            'project': self.project.id,
            'sort_number': 0,
            'logo': logo
        }
        response = self.client.post(reverse('sponsor-create'), post_data)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorDeleteView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsor-delete', kwargs={
            'slug': self.sponsor.slug
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsor/delete.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorDeleteView_no_login(self):

        response = self.client.get(reverse('sponsor-delete', kwargs={
            'slug': self.sponsor.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorDelete_with_login(self):

        sponsor_to_delete = SponsorF.create(project=self.project)
        self.client.login(username='timlinux', password='password')
        response = self.client.post(reverse('sponsor-delete', kwargs={
            'slug': sponsor_to_delete.slug
        }), {})
        self.assertRedirects(response, reverse('sponsor-list'))

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorDelete_no_login(self):

        sponsor_to_delete = SponsorF.create(
            project=self.project
        )
        response = self.client.post(reverse('sponsor-delete', kwargs={
            'slug': sponsor_to_delete.slug
        }))
        self.assertEqual(response.status_code, 302)


class TestSponsorshipPeriodViews(TestCase):
    """Tests that SponsorshipPeriod views work."""

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
        self.sponsor = SponsorF.create(
                project=self.project,
                name='Kartoza')
        self.sponsorship_level = SponsorshipLevelF.create(
                project=self.project,
                name='Gold')
        self.sponsorship_period = SponsorshipPeriodF.create(
            project=self.project,
            sponsor=self.sponsor,
            sponsorship_level=self.sponsorship_level,
            approved=True)
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def tearDown(self):
        """
        Teardown after each test.

        :return:
        """
        self.project.delete()
        self.sponsor.delete()
        self.sponsorship_level.delete()
        self.sponsorship_period.delete()
        self.user.delete()

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodListView(self):
        """Test SponsorshipPeriod list view."""
        response = self.client.get(reverse('sponsorshipperiod-list'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_period/list.html',
            u'changes/sponsorshipperiod_list.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodCreateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(reverse('sponsorshipperiod-create'))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_period/create.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodCreateView_no_login(self):

        response = self.client.get(reverse('sponsorshipperiod-create'))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodCreate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'sponsor': self.sponsor.id,
            'sponsorshiplevel': self.sponsorship_level.id,
            'author': self.user.id
        }
        response = self.client.post(
            reverse(
                'sponsorshipperiod-create'), post_data)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodCreate_no_login(self):

        post_data = {
            'sponsor': self.sponsor.id,
            'sponsorship_level': self.sponsorship_level.id
        }
        response = self.client.post(
            reverse('sponsorshipperiod-create'), post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodUpdateView_with_login(self):

        self.client.login(username='timlinux', password='password')
        response = self.client.get(
            reverse('sponsorshipperiod-update', kwargs={
                'slug': self.sponsorship_period.slug
            }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'sponsorship_period/update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodUpdateView_no_login(self):

        response = self.client.get(reverse('sponsorshipperiod-update', kwargs={
            'slug': self.sponsorship_period.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodUpdate_with_login(self):

        self.client.login(username='timlinux', password='password')
        post_data = {
            'sponsor': self.sponsor.id,
            'sponsorshiplevel': self.sponsorship_level.id,
            'author': self.user.id
        }
        response = self.client.post(
            reverse('sponsorshipperiod-update', kwargs={
                'slug': self.sponsorship_period.slug
            }), post_data)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodUpdate_no_login(self):

        post_data = {
            'sponsor': self.sponsor.id,
            'sponsorshiplevel': self.sponsorship_level.id
        }
        response = self.client.post(
            reverse('sponsorshipperiod-update', kwargs={
                'slug': self.sponsorship_period.slug
            }), post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodDeleteView_no_login(self):

        response = self.client.get(reverse('sponsorshipperiod-delete', kwargs={
            'slug': self.sponsorship_period.slug
        }))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_SponsorshipPeriodDelete_no_login(self):

        response = self.client.post(
            reverse('sponsorshipperiod-delete', kwargs={
                'slug': self.sponsorship_period.slug
            }))
        self.assertEqual(response.status_code, 302)
