# coding=utf-8
"""Project model used by all apps."""
import logging
import os
import re
import string

from base.models.organisation import Organisation
from changes.models.version import Version
from colorfield.fields import ColorField
from core.settings.contrib import STOP_WORDS
from django.conf import settings
from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from unidecode import unidecode

logger = logging.getLogger(__name__)


class ApprovedProjectManager(models.Manager):
    """Custom project manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(ApprovedProjectManager, self).get_queryset().filter(approved=True)


class UnapprovedProjectManager(models.Manager):
    """Custom project manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator."""
        return (
            super(UnapprovedProjectManager, self).get_queryset().filter(approved=False)
        )


class PublicProjectManager(models.Manager):
    """Custom project manager that shows only public and approved projects."""

    def get_queryset(self):
        """Query set generator."""
        return (
            super(PublicProjectManager, self)
            .get_queryset()
            .filter(private=False)
            .filter(approved=True)
        )


def validate_gitter_room_name(value):
    """Ensure user enter proper gitter room name

    :param value: string input
    :raises: ValidationError
    """
    invalid_chars = set(string.punctuation.replace("/", ""))
    pattern = re.compile("^(\w+\/\w+)$")
    if any(char in invalid_chars for char in value) or not pattern.match(value):
        raise ValidationError(
            _("%(value)s is not proper gitter room name"),
            params={"value": value},
        )


def get_default_organisation():
    # The owner of the default organisation is purposely empty because in the
    # unittest it raises error since there are duplicates. But the owner of
    # default organisation can be changed in the live site.

    organisation = Organisation.objects.get_or_create(name="Public", approved=True)[0]
    return organisation.pk


class Project(models.Model):
    """A project model e.g. QGIS, InaSAFE etc."""

    EUR = "EUR"
    USD = "USD"
    CURRENCY_CHOICES = [(USD, "$"), (EUR, "€")]

    name = models.CharField(
        help_text=_("Name of this project."),
        max_length=255,
        null=False,
        blank=False,
        unique=True,
    )

    description = models.CharField(
        help_text=_("A short description for the project"),
        max_length=500,
        blank=True,
        null=True,
    )

    precis = models.TextField(
        help_text=_("A detailed summary of the project. Markdown is supported."),
        max_length=2000,
        blank=True,
        null=True,
    )

    image_file = models.ImageField(
        help_text=_(
            "A logo image for this project. Most browsers support dragging "
            'the image directly on to the "Choose File" button above. The '
            "ideal size for your image is 512 x 512 pixels."
        ),
        upload_to=os.path.join(MEDIA_ROOT, "images/projects"),
        blank=True,
    )

    accent_color = ColorField(
        help_text=_("A color represent the project color"),
        blank=True,
        null=True,
        default="#FF0000",
    )

    project_representative_signature = models.ImageField(
        help_text=_(
            "This signature will be used on invoices and certificates. "
            "Most browsers support dragging "
            'the image directly on to the "Choose File" button above.'
        ),
        upload_to=os.path.join(MEDIA_ROOT, "images/projects/signatures"),
        blank=True,
    )

    approved = models.BooleanField(
        help_text=_("Whether this project has been approved for use yet."),
        default=False,
    )

    private = models.BooleanField(
        help_text=_("Only visible to logged-in users?"), default=False
    )

    project_url = models.URLField(
        help_text="Optional URL for this project\s home page", blank=True, null=True
    )

    project_repository_url = models.URLField(
        help_text=_(
            "A repository URL for this project. "
            "For instance a path to the project's GitHub repository."
        ),
        blank=True,
        null=True,
    )

    sponsorship_programme = models.TextField(
        help_text=_(
            "Please describe the sponsorship programme for this project "
            "(if any). Markdown is supported"
        ),
        max_length=10000,
        blank=True,
        null=True,
    )

    sponsorship_managers = models.ManyToManyField(
        User,
        related_name="sponsorship_managers",
        verbose_name="Sustaining member managers",
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            "Managers of the sponsorship in this project. "
            "They will be allowed to approve sustaining member entries in the "
            "moderation queue."
        ),
    )

    # Organisation where a project belongs, when the organisation is deleted,
    #  the project will automatically belongs to default organisation.
    organisation = models.ForeignKey(
        Organisation,
        default=get_default_organisation,
        null=True,
        on_delete=models.SET_DEFAULT,
    )

    project_representative = models.ForeignKey(
        User,
        related_name="project_representative",
        help_text=_(
            "Project representative. "
            "This name will be used on invoices and certificates. "
        ),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,  # This is needed to populate existing database.
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    objects = models.Manager()
    approved_objects = ApprovedProjectManager()
    unapproved_objects = UnapprovedProjectManager()
    public_objects = PublicProjectManager()

    gitter_room = models.CharField(
        help_text=_("Gitter room name, e.g. gitterhq/sandbox"),
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_gitter_room_name],
    )

    is_sustaining_members = models.BooleanField(
        help_text=_("Whether this Project has Sustaining Members."), default=True
    )

    external_reviewer_invitation = models.TextField(
        help_text=_(
            "Standard text for external reviewer of what " "they are expected to do."
        ),
        default="You have been invited to review this organisation.",
        max_length=10000,
        blank=True,
        null=True,
    )

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""

        app_label = "base"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        """Overloaded save method.

        :param args:
        :param kwargs:
        """
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(" ".join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        """Return URL to project detail page

        :return: URL
        :rtype: str

        """
        return reverse("project-detail", kwargs={"slug": self.slug})

    def versions(self):
        """Get all the versions for this project."""
        qs = Version.objects.filter(project=self).order_by("-padded_version")
        return qs

    def latest_versions(self):
        """Get the latest version.

        How many versions returned is determined by the pagination threshold.

        :returns: List of versions.
        :rtype: list"""
        return self.versions()[: settings.PROJECT_VERSION_LIST_SIZE]

    @staticmethod
    def pagination_threshold():
        """Find out how many versions to list per page.

        :returns: The count of items to show per page as defined in
            settings.PROJECT_VERSION_LIST_SIZE.
        :rtype: int
        """
        return settings.PROJECT_VERSION_LIST_SIZE

    def pagination_threshold_exceeded(self):
        """Check if project version count exceeds pagination threshold.

        :returns: Flag indicating if there are more versions than
            self.threshold.
        :rtype: bool
        """
        if self.versions().count() >= settings.PROJECT_VERSION_LIST_SIZE:
            return True
        else:
            return False


class ProjectScreenshot(models.Model):
    """A model to store a screenshot linked to a project."""

    project = models.ForeignKey(
        Project, related_name="screenshots", on_delete=models.CASCADE
    )
    screenshot = models.ImageField(
        help_text=_("A project screenshot."),
        upload_to=os.path.join(MEDIA_ROOT, "images/projects/screenshots"),
        blank=True,
    )
