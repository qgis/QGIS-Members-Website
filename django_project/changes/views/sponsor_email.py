from changes.forms import SponsorEmailForm
from changes.models import SponsorEmail
from changes.permissions import CustomStaffuserRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    View,
)
from pure_pagination.mixins import PaginationMixin


class SponsorEmailMixin:
    """Mixin class to provide standard settings for SponsorEmail views."""

    model = SponsorEmail
    form_class = SponsorEmailForm


class SponsorEmailListView(
    CustomStaffuserRequiredMixin, PaginationMixin, SponsorEmailMixin, ListView
):
    """View to list all SponsorEmail objects with pagination and filtering."""

    model = SponsorEmail
    template_name = "sponsor_email/list.html"
    context_object_name = "sponsoremails"
    ordering = ["-created_at"]
    paginate_by = 10

    def get_queryset(self):
        """Return the queryset of SponsorEmail objects."""
        return SponsorEmail.objects.filter(is_deleted=False).order_by("-created_at")

    def get_context_data(self, **kwargs):
        """Add additional context to the template."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Sponsor Emails"
        return context


class SponsorEmailCreateView(
    CustomStaffuserRequiredMixin, SponsorEmailMixin, CreateView
):
    """View to create a new SponsorEmail object."""

    template_name = "sponsor_email/create.html"

    def get_success_url(self):
        """Redirect to the list of SponsorEmail objects after creation."""
        return reverse("sponsor-email-list")

    def get_context_data(self, **kwargs):
        """Add additional context to the template."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Sponsor Email"
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SponsorEmailCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form submission for creating a new SponsorEmail."""
        response = super().form_valid(form)
        recipients = self.object.get_all_recipients()
        if recipients["to"]:
            self.object.send_email(recipients)
            messages.success(
                self.request,
                "Sponsor email saved successfully. It should be sent shortly.",
            )
        else:
            messages.warning(
                self.request,
                (
                    "No recipients found. Email was not sent.<br>"
                    "Please ensure that at least one sustaining member in the selected levels "
                    "has the option <strong>'Receive News and Crowdfunding Information'</strong> checked."
                    "You can update this setting in the sustaining member's profile."
                ),
            )
        return response


class SponsorEmailResendView(CustomStaffuserRequiredMixin, View):
    """View to confirm and resend a SponsorEmail."""

    template_name = "sponsor_email/resend.html"

    def get(self, request, *args, **kwargs):
        sponsor_email = get_object_or_404(
            SponsorEmail, pk=kwargs["pk"], is_deleted=False
        )
        context = {
            "sponsor_email": sponsor_email,
            "title": "Resend Sponsor Email",
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        sponsor_email = get_object_or_404(
            SponsorEmail, pk=kwargs["pk"], is_deleted=False
        )
        recipients = sponsor_email.get_all_recipients()
        if recipients["to"]:
            sponsor_email.send_email(recipients)
            messages.success(
                request, "Sponsor email saved successfully. It should be sent shortly."
            )
        else:
            messages.warning(
                request,
                (
                    "No recipients found. Email was not sent.<br>"
                    "Please ensure that at least one sustaining member in the selected levels "
                    "has the option <strong>'Receive News and Crowdfunding Information'</strong> checked."
                    "You can update this setting in the sustaining member's profile."
                ),
            )
        return redirect("sponsor-email-detail", pk=sponsor_email.pk)


class SponsorEmailDetailView(CustomStaffuserRequiredMixin, DetailView):
    """View to display details of a specific SponsorEmail object."""

    template_name = "sponsor_email/details.html"
    context_object_name = "sponsor_email"
    model = SponsorEmail

    def get_context_data(self, **kwargs):
        """Add additional context to the template."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Sponsor Email Detail"
        context["sender_email"] = settings.DEFAULT_FROM_EMAIL
        return context

    def get_object(self, queryset=None):
        """Get the SponsorEmail object for the detail view."""
        return SponsorEmail.objects.get(pk=self.kwargs["pk"], is_deleted=False)


class SponsorEmailDeleteView(CustomStaffuserRequiredMixin, View):
    """View to soft delete a SponsorEmail object (does not really delete the entry)."""

    template_name = "sponsor_email/delete.html"

    def get(self, request, *args, **kwargs):
        sponsor_email = get_object_or_404(
            SponsorEmail, pk=kwargs["pk"], is_deleted=False
        )
        context = {
            "sponsor_email": sponsor_email,
            "title": "Delete Sponsor Email",
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        sponsor_email = get_object_or_404(
            SponsorEmail, pk=kwargs["pk"], is_deleted=False
        )
        sponsor_email.soft_delete()
        messages.success(request, "Sponsor email deleted (soft delete) successfully.")
        return redirect("sponsor-email-list")
