# coding=utf-8
"""Factories for creating model instances for testing."""

from datetime import date, datetime, timedelta

import factory
import factory.fuzzy
from changes.models.category import Category
from changes.models.entry import Entry
from changes.models.sponsor import Sponsor
from changes.models.sponsorship_level import SponsorshipLevel
from changes.models.sponsorship_period import SponsorshipPeriod
from changes.models.version import Version
from core.model_factories import UserF
from django.utils import timezone


class CategoryF(factory.django.DjangoModelFactory):
    """
    Category model factory
    """

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "Test Category %s" % n)
    sort_number = factory.Sequence(lambda n: n)
    project = factory.SubFactory("base.tests.model_factories.ProjectF")


class EntryF(factory.django.DjangoModelFactory):
    """
    Entry model factory
    """

    class Meta:
        model = Entry

    title = factory.Sequence(lambda n: "This is a great title: %s" % n)
    description = "This description is really only here for testing"
    image_file = factory.django.ImageField(color="blue")
    image_credits = "The credits go to dodobas"
    author = factory.SubFactory(UserF)
    version = factory.SubFactory("changes.tests.model_factories.VersionF")
    category = factory.SubFactory("changes.tests.model_factories.CategoryF")


class VersionF(factory.django.DjangoModelFactory):
    """
    Version model factory
    """

    class Meta:
        model = Version

    padded_version = factory.Sequence(lambda n: "100001100 %s" % n)
    image_file = factory.django.ImageField(color="green")
    author = factory.SubFactory(UserF)
    description = "This description is really only here for testing"
    project = factory.SubFactory("base.tests.model_factories.ProjectF")


class SponsorF(factory.django.DjangoModelFactory):
    """
    Sponsors model factory
    """

    class Meta:
        model = Sponsor

    name = factory.Sequence(lambda n: "Test Sponsor Name %s" % n)
    address = factory.Sequence(lambda n: "Address\nline2\n%s" % n)
    country = "za"
    sponsor_url = factory.Sequence(lambda n: "Test URL %s" % n)
    contact_person = factory.Sequence(lambda n: "Test Contact Person %s" % n)
    sponsor_email = factory.Sequence(lambda n: "Test Sponsor Email %s" % n)
    approved = True
    author = factory.SubFactory(UserF)
    logo = factory.django.ImageField(color="green")
    agreement = factory.django.ImageField(color="green")
    project = factory.SubFactory("base.tests.model_factories.ProjectF")


class SponsorshipLevelF(factory.django.DjangoModelFactory):
    """
    Sponsorship Level model factory
    """

    class Meta:
        model = SponsorshipLevel

    name = factory.Sequence(lambda n: "Test Sponsorship level %s" % n)
    currency = factory.Sequence(lambda n: "Test Currency %s" % n)
    approved = True
    author = factory.SubFactory(UserF)
    value = factory.Sequence(lambda n: n)
    logo = factory.django.ImageField(color="green")
    project = factory.SubFactory("base.tests.model_factories.ProjectF")


class SponsorshipPeriodF(factory.django.DjangoModelFactory):
    """
    Sponsorship Period model factory
    """

    class Meta:
        model = SponsorshipPeriod

    start_date = factory.fuzzy.FuzzyDate(date(2014, 1, 1))
    end_date = factory.fuzzy.FuzzyDate(
        start_date=datetime.date(datetime.now()) + timedelta(days=365),
        end_date=datetime.date(datetime.now()) + timedelta(days=750),
    )
    approved = True
    author = factory.SubFactory(UserF)
    project = factory.SubFactory("base.tests.model_factories.ProjectF")
    sponsor = factory.SubFactory("changes.tests.model_factories.SponsorF")
    sponsorship_level = factory.SubFactory(
        "changes.tests.model_factories.SponsorshipLevelF"
    )


class SponsorEmailF(factory.django.DjangoModelFactory):
    """
    SponsorEmail model factory
    """

    class Meta:
        model = "changes.SponsorEmail"

    sender = factory.SubFactory(UserF)
    subject = factory.Sequence(lambda n: "Test Sponsor Email Subject %s" % n)
    body = "This is the body of the test sponsor email"
    email_type = "both"
    cc = ""
    status = "draft"
    is_deleted = False
    created_at = factory.LazyFunction(lambda: timezone.now())
    sent_at = None

    @factory.post_generation
    def sponsor_levels(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for level in extracted:
                self.sponsor_levels.add(level)
