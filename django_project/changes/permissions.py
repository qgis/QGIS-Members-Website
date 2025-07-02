from braces.views import StaffuserRequiredMixin
from django.http import Http404


class CustomStaffuserRequiredMixin(StaffuserRequiredMixin):

    """Fix redirect loop when user is already authenticated but non staff."""

    def no_permissions_fail(self, request=None):
        """
        Called when the user has no permissions and no exception was raised.
        """
        if not request.user.is_authenticated:
            return super(
                CustomStaffuserRequiredMixin, self).no_permissions_fail(
                request)

        raise Http404('Sorry! You have to be staff to open this page.')