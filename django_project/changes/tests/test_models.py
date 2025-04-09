# coding=utf-8
"""Tests for models."""
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from changes.tests.model_factories import (
    CategoryF,
    EntryF,
    VersionF,
    SponsorshipLevelF,
    SponsorF,
    SponsorshipPeriodF)
from base.tests.model_factories import ProjectF


class TestSponsorCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Sponsor_create(self):
        """
        Tests Sponsor model creation
        """
        model = SponsorF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_Sponsor_read(self):
        """
        Tests Sponsor model read
        """
        model = SponsorF.create(
            name=u'Custom Sponsor'
        )

        self.assertTrue(model.name == 'Custom Sponsor')

    def test_Sponsor_update(self):
        """
        Tests Sponsor model update
        """
        model = SponsorF.create()
        new_model_data = {
            'name': u'New Sponsor Name',
            'sponsor_url': u'New Sponsor URL',
            'approved': False,
            'private': True,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Sponsor_delete(self):
        """
        Tests Sponsor model delete
        """
        model = SponsorF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestSponsorshipLevelCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SponsorshipLevel_create(self):
        """
        Tests Sponsorship Level model creation
        """
        model = SponsorshipLevelF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_SponsorshipLevel_read(self):
        """
        Tests Sponsorship Level model read
        """
        model = SponsorshipLevelF.create(
            name=u'Custom SponsorshipLevel'
        )

        self.assertTrue(model.name == 'Custom SponsorshipLevel')

    def test_SponsorshipLevel_update(self):
        """
        Tests Sponsorship Level model update
        """
        model = SponsorshipLevelF.create()
        new_model_data = {
            'name': u'New Sponsorship Level Name',
            'currency': u'IDR',
            'approved': False,
            'private': True,
            'logo_width': 100,
            'logo_height': 100
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_SponsorshipLevel_delete(self):
        """
        Tests SponsorshipLevel model delete
        """
        model = SponsorshipLevelF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestSponsorshipPeriodCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SponsorshipPeriod_create(self):
        """
        Tests Sponsorship Period model creation
        """
        model = SponsorshipPeriodF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.start_date is not None)

    def test_SponsorshipPeriod_read(self):
        """
        Tests Sponsorship Period model read
        """
        model = SponsorshipPeriodF.create(
            start_date=datetime(2016, 1, 1)
        )

        self.assertTrue(model.start_date == datetime(2016, 1, 1))

    def test_SponsorshipPeriod_update(self):
        """
        Tests Sponsorship Period model update
        """
        model = SponsorshipPeriodF.create()
        new_model_data = {
            'start_date': datetime(2016, 1, 1),
            'approved': False,
            'private': True,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_SponsorshipPeriod_delete(self):
        """
        Tests SponsorshipPeriod model delete
        """
        model = SponsorshipPeriodF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestValidateEmailAddress(TestCase):
    """Test validate_email_address function."""

    def test_validation_failed_must_raise_ValidationError(self):
        from changes.models import validate_email_address
        email = 'email@wrongdomain'
        msg = f'{email} is not a valid email address'
        with self.assertRaisesMessage(ValidationError, msg):
            validate_email_address(email)
