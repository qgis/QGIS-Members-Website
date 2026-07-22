# models.py
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone


class SponsorEmail(models.Model):
    """
    Represents an email message sent or saved for sustaining (sponsor) members.
    This model supports targeting sponsors by sponsorship level, sending to admin/tech/both emails,
    and includes soft deletion, CC support, and recipient filtering based on sponsor preferences.
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    EMAIL_TYPE_CHOICES = [
        ("admin", "Admin Email Only"),
        ("tech", "Tech Email Only"),
        ("both", "Both Admin and Tech Emails"),
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_emails"
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sponsor_levels = models.ManyToManyField(
        "SponsorshipLevel",
        related_name="emails",
        help_text="Select sponsor levels to receive this email",
    )
    email_type = models.CharField(
        max_length=5,
        choices=EMAIL_TYPE_CHOICES,
        default="both",
        help_text="Select which email addresses to send to for each sponsor",
    )
    cc = models.TextField(blank=True, help_text="Comma separated list of CC emails")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sponsor Email"
        verbose_name_plural = "Sponsor Emails"

    def __str__(self):
        return f"{self.subject} - {self.get_status_display()}"

    def clean(self):
        """Validate CC field"""
        if self.cc:
            email_list = [e.strip() for e in self.cc.split(",") if e.strip()]
            for email in email_list:
                try:
                    validate_email(email)
                except ValidationError:
                    raise ValidationError(
                        {"cc": f"'{email}' is not a valid email address"}
                    )

    def get_recipients(self):
        """Get all sponsors from the selected levels with currently active periods"""
        from changes.models import Sponsor  # Import here to avoid circular imports
        from changes.models import (
            SponsorshipPeriod,  # Import here to avoid circular imports
        )

        now = timezone.now().date()
        active_periods = SponsorshipPeriod.objects.filter(
            sponsorship_level__in=self.sponsor_levels.all(),
            start_date__lte=now,
            end_date__gte=now,
        ).select_related("sponsor")
        sponsor_ids = active_periods.values_list("sponsor_id", flat=True).distinct()
        sponsors = Sponsor.objects.filter(id__in=sponsor_ids)
        return sponsors

    def get_recipient_emails(self):
        """Get email addresses based on selected type (admin/tech/both), excluding sponsors with receive_news=False"""
        sponsors = self.get_recipients()
        # Exclude sponsors with receive_news=False
        sponsors = sponsors.filter(receive_news=True)
        emails = []

        if self.email_type in ["admin", "both"]:
            admin_emails = sponsors.exclude(sponsor_email__exact="").values_list(
                "sponsor_email", flat=True
            )
            emails.extend([e for e in admin_emails if e])

        if self.email_type in ["tech", "both"]:
            tech_emails = sponsors.exclude(tech_email__exact="").values_list(
                "tech_email", flat=True
            )
            emails.extend([e for e in tech_emails if e])

        return list(set(emails))  # Remove duplicates

    def get_cc_list(self):
        """Return CC as list of emails"""
        return [e.strip() for e in self.cc.split(",") if e.strip()] if self.cc else []

    def get_all_recipients(self):
        """Combine sponsor emails and CC emails"""
        recipient_emails = self.get_recipient_emails()
        cc_emails = self.get_cc_list()
        return {"to": recipient_emails, "cc": cc_emails}

    def soft_delete(self):
        """Mark the email as deleted instead of actually deleting it"""
        self.is_deleted = True
        self.save()

    def send_email(self, recipients):
        """
        Send the email to the recipients.
        Handles errors and updates status accordingly.
        """
        from smtplib import SMTPException

        from django.core.mail import BadHeaderError, EmailMessage

        try:
            email = EmailMessage(
                subject=self.subject,
                body=self.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                bcc=recipients["to"],
                cc=recipients["cc"],
            )
            if not settings.DEBUG:
                email.send()
            self.status = "sent"
            self.sent_at = timezone.now()
        except (BadHeaderError, SMTPException, Exception):
            self.status = "failed"
        self.save()

    def get_type_display(self):
        """Get a human-readable display of the email type."""
        return dict(self.EMAIL_TYPE_CHOICES).get(self.email_type, "Unknown")
