from changes.forms import SponsorEmailForm
from changes.models import SponsorEmail
from changes.permissions import CustomStaffuserRequiredMixin
from django.views.generic import CreateView, ListView
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
        return self.request.path_info

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
        if recipients:
            self.object.send_email(recipients)
        return response
