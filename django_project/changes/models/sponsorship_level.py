# coding=utf-8

import os

from core.settings.contrib import STOP_WORDS
from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

__author__ = "rischan"


class ApprovedSponsorshipLevelManager(models.Manager):
    """Custom sponsor manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator."""
        return (
            super(ApprovedSponsorshipLevelManager, self)
            .get_queryset()
            .filter(approved=True)
        )


class UnapprovedSponsorshipLevelManager(models.Manager):
    """Custom sponsor manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator."""
        return (
            super(UnapprovedSponsorshipLevelManager, self)
            .get_queryset()
            .filter(approved=False)
        )


class SponsorshipLevel(models.Model):
    """A sponsor model e.g. gui, backend, web site etc."""

    id = models.AutoField(
        help_text="Unique ID for this sustaining membership level.",
        primary_key=True,
        unique=True,
        null=False,
        blank=False,
    )
    name = models.CharField(
        help_text="Name of sustaining membership level. e.g. Gold, Bronze, etc",
        max_length=255,
        null=False,
        blank=False,
        unique=False,
    )

    value = models.IntegerField(
        help_text="Amount of money associated with this sustaining membership level.",
        blank=False,
        null=False,
        unique=False,
    )

    currency = models.CharField(
        help_text="The currency which associated with "
        "this sustaining membership level.",
        max_length=255,
        null=False,
        blank=False,
        unique=False,
    )

    logo = models.ImageField(
        help_text=(
            "An image of sustaining membership level logo e.g. a bronze medal."
            "Most browsers support dragging the image directly on to the "
            '"Choose File" button above.'
        ),
        upload_to=os.path.join(MEDIA_ROOT, "images/projects"),
        blank=False,
    )

    logo_width = models.IntegerField(
        help_text=("Enter the width of the icon that should be used on the changelog"),
        blank=False,
        null=False,
        default=100,
    )

    logo_height = models.IntegerField(
        help_text=("Enter the height of the icon that should be used on the changelog"),
        blank=False,
        null=False,
        default=100,
    )

    approved = models.BooleanField(
        help_text=_(
            "Whether this sustaining membership level has been approved for use by "
            "the project owner."
        ),
        default=False,
    )

    subscription_plan = models.ForeignKey(
        "djstripe.Plan",
        help_text=("A Stripe subscription plan contains the pricing information"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    project = models.ForeignKey("base.Project", on_delete=models.CASCADE)
    objects = models.Manager()
    approved_objects = ApprovedSponsorshipLevelManager()
    unapproved_objects = UnapprovedSponsorshipLevelManager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the sponsor class."""

        constraints = [
            models.UniqueConstraint(fields=["id"], name="unique_sponsorshiplevel_id")
        ]
        unique_together = (("name", "project"), ("project", "slug"))
        app_label = "changes"
        ordering = ["project", "-value"]
        verbose_name = "Sustaining Member Level"
        verbose_name_plural = "Sustaining Member Levels"

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = " ".join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(SponsorshipLevel, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s : %s %s" % (self.name, self.value, self.currency)

    def __str__(self):
        return "%s : %s %s" % (self.name, self.value, self.currency)

    def get_absolute_url(self):
        return reverse(
            "sponsorshiplevel-detail",
            kwargs={"slug": self.slug, "project_slug": self.project.slug},
        )
