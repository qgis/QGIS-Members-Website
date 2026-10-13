from changes.views.category import *
from changes.views.changelog_github import *
from changes.views.entry import *
from changes.views.sponsor import *
from changes.views.sponsor_email import *
from changes.views.sponsorship_level import *
from changes.views.sponsorship_period import *
from changes.views.sustaining_member import *
from changes.views.version import *


def redirect_root(request):
    return redirect("sponsor-list")
