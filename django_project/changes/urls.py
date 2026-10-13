# coding=utf-8
# flake8: noqa
"""Urls for changelog application."""

from changes.api_views.lock_version import LockVersion, UnlockVersion
from django.conf import settings
from django.urls import include
from django.urls import re_path as url  # noqa
from django.views.static import serve

from .feeds.entry import AtomEntryFeed, RssEntryFeed
from .feeds.sponsor import (
    AtomPastSponsorFeed,
    AtomSponsorFeed,
    JSONPastSponsorFeed,
    JSONSponsorFeed,
    RssPastSponsorFeed,
    RssSponsorFeed,
)
from .feeds.version import AtomVersionFeed, RssVersionFeed
from .views import (  # Sponsor; Sponsorship Level; Sponsorship Period; Sponsor Email
    ApproveSponsorshipLevelView,
    ApproveSponsorshipPeriodView,
    ApproveSponsorView,
    FutureSponsorListView,
    GenerateSponsorPDFView,
    JSONSponsorListView,
    JSONSponsorshipLevelListView,
    JSONSponsorshipPeriodListView,
    PastSponsorListView,
    PendingSponsorListView,
    PendingSponsorshipLevelListView,
    PendingSponsorshipPeriodListView,
    RejectedSustainingMemberList,
    RejectSponsorView,
    SponsorCreateView,
    SponsorDeleteView,
    SponsorDetailView,
    SponsorEmailCreateView,
    SponsorEmailDeleteView,
    SponsorEmailDetailView,
    SponsorEmailListView,
    SponsorEmailResendView,
    SponsorListView,
    SponsorshipLevelCreateView,
    SponsorshipLevelDeleteView,
    SponsorshipLevelDetailView,
    SponsorshipLevelListView,
    SponsorshipLevelUpdateView,
    SponsorshipPeriodCreateView,
    SponsorshipPeriodDeleteView,
    SponsorshipPeriodDetailView,
    SponsorshipPeriodListView,
    SponsorshipPeriodUpdateView,
    SponsorUpdateView,
    SustainingMemberPeriodCreateView,
    SustainingMemberPeriodUpdateView,
    SustainingMembership,
    SustainingMemberUpdateView,
    generate_sponsor_cloud,
    redirect_root,
)

urlpatterns = [
    # Root
    url(r"^$", redirect_root, name="homepage"),
    # Category management
    url(
        r"^member/(?P<slug>[\w-]+)/invoice/$",
        view=GenerateSponsorPDFView.as_view(),
        name="sponsor-invoice",
    ),
    # Feeds sponsors in a specific project
    url(r"^members/rss/$", view=RssSponsorFeed(), name="sponsor-rss-feed"),
    url(
        r"^past-members/rss/$", view=RssPastSponsorFeed(), name="past-sponsor-rss-feed"
    ),
    url(r"^members/atom/$", view=AtomSponsorFeed(), name="sponsor-atom-feed"),
    url(
        r"^past-members/atom/$",
        view=AtomPastSponsorFeed(),
        name="past-sponsor-atom-feed",
    ),
    url(r"^members/json/$", view=JSONSponsorFeed(), name="sponsor-json-feed"),
    url(
        r"^past-members/json/$",
        view=JSONPastSponsorFeed(),
        name="past-sponsor-json-feed",
    ),
    # Sponsor management
    # This view is only accessible via ajax
    url(
        r"^json-member/list/(?P<version>\d+)/$",
        view=JSONSponsorListView.as_view(),
        name="json-sponsor-list",
    ),
    url(
        r"^pending-members/list/$",
        view=PendingSponsorListView.as_view(),
        name="pending-sponsor-list",
    ),
    url(
        r"^sustaining-members-rejected/list/$",
        view=RejectedSustainingMemberList.as_view(),
        name="sustaining-members-rejected-list",
    ),
    url(
        r"^approve-member/(?P<slug>[\w-]+)/$",
        view=ApproveSponsorView.as_view(),
        name="sponsor-approve",
    ),
    url(
        r"^reject-member/(?P<member_id>\d+)/$",
        view=RejectSponsorView.as_view(),
        name="sponsor-reject",
    ),
    url(r"^members/list/$", view=SponsorListView.as_view(), name="sponsor-list"),
    url(
        r"^past-members/list/$",
        view=PastSponsorListView.as_view(),
        name="past-sponsor-list",
    ),
    url(
        r"^future-members/list/$",
        view=FutureSponsorListView.as_view(),
        name="future-sponsor-list",
    ),
    url(
        r"^member/(?P<slug>[\w-]+)/$",
        view=SponsorDetailView.as_view(),
        name="sponsor-detail",
    ),
    url(
        r"^member/(?P<slug>[\w-]+)/delete/$",
        view=SponsorDeleteView.as_view(),
        name="sponsor-delete",
    ),
    url(r"^create-member/$", view=SponsorCreateView.as_view(), name="sponsor-create"),
    url(
        r"^member/(?P<slug>[\w-]+)/update/$",
        view=SponsorUpdateView.as_view(),
        name="sponsor-update",
    ),
    # Sponsorship Level management
    # This view is only accessible via ajax
    url(
        r"^json-membershiplevel/list/(?P<version>\d+)/$",
        view=JSONSponsorshipLevelListView.as_view(),
        name="json-sponsorshiplevel-list",
    ),
    url(
        r"^pending-membershiplevel/list/$",
        view=PendingSponsorshipLevelListView.as_view(),
        name="pending-sponsorshiplevel-list",
    ),
    url(
        r"^approve-membershiplevel/(?P<slug>[\w-]+)/$",
        view=ApproveSponsorshipLevelView.as_view(),
        name="sponsorshiplevel-approve",
    ),
    url(
        r"^membershiplevel/list/$",
        view=SponsorshipLevelListView.as_view(),
        name="sponsorshiplevel-list",
    ),
    url(
        r"^membershiplevel/(?P<slug>[\w-]+)/$",
        view=SponsorshipLevelDetailView.as_view(),
        name="sponsorshiplevel-detail",
    ),
    url(
        r"^membershiplevel/(?P<slug>[\w-]+)/delete/$",
        view=SponsorshipLevelDeleteView.as_view(),
        name="sponsorshiplevel-delete",
    ),
    url(
        r"^create-membershiplevel/$",
        view=SponsorshipLevelCreateView.as_view(),
        name="sponsorshiplevel-create",
    ),
    url(
        r"^membershiplevel/(?P<slug>[\w-]+)/update/$",
        view=SponsorshipLevelUpdateView.as_view(),
        name="sponsorshiplevel-update",
    ),
    # Sponsorship Period management
    # This view is only accessible via ajax
    url(
        r"^json-membershipperiod/list/(?P<version>\d+)/$",
        view=JSONSponsorshipPeriodListView.as_view(),
        name="json-sponsorshipperiod-list",
    ),
    url(
        r"^pending-membershipperiod/list/$",
        view=PendingSponsorshipPeriodListView.as_view(),
        name="pending-sponsorshipperiod-list",
    ),
    url(
        r"^approve-membershipperiod/(?P<slug>[\w-]+)/$",
        view=ApproveSponsorshipPeriodView.as_view(),
        name="sponsorshipperiod-approve",
    ),
    url(
        r"^membershipperiod/list/$",
        view=SponsorshipPeriodListView.as_view(),
        name="sponsorshipperiod-list",
    ),
    url(
        r"^membershipperiod/(?P<slug>[\w-]+)/$",
        view=SponsorshipPeriodDetailView.as_view(),
        name="sponsorshipperiod-detail",
    ),
    url(
        r"^membershipperiod/(?P<slug>[\w-]+)/delete/$",
        view=SponsorshipPeriodDeleteView.as_view(),
        name="sponsorshipperiod-delete",
    ),
    url(
        r"^create-membershipperiod/$",
        view=SponsorshipPeriodCreateView.as_view(),
        name="sponsorshipperiod-create",
    ),
    url(
        r"^membershipperiod/(?P<slug>[\w-]+)/update/$",
        view=SponsorshipPeriodUpdateView.as_view(),
        name="sponsorshipperiod-update",
    ),
    # Sponsor Cloud
    url(r"^member-cloud/$", view=generate_sponsor_cloud, name="sponsor-cloud"),
    # Sustaining member
    url(
        r"^membership/$",
        view=SustainingMembership.as_view(),
        name="sustaining-membership",
    ),
    url(
        r"^sustaining-member/update/(?P<member_id>\d+)/$",
        view=SustainingMemberUpdateView.as_view(),
        name="sustaining-member-update",
    ),
    url(
        r"^sustaining-member-period/create/(?P<member_id>\d+)/$",
        view=SustainingMemberPeriodCreateView.as_view(),
        name="sustaining-member-period-create",
    ),
    url(
        r"^sustaining-member-period/update/(?P<member_id>\d+)/$",
        view=SustainingMemberPeriodUpdateView.as_view(),
        name="sustaining-member-period-update",
    ),
    # Sponsor Email
    url(
        r"^email/list/$", view=SponsorEmailListView.as_view(), name="sponsor-email-list"
    ),
    url(
        r"^email/create/$",
        view=SponsorEmailCreateView.as_view(),
        name="sponsor-email-create",
    ),
    url(
        r"^email/(?P<pk>\d+)/$",
        view=SponsorEmailDetailView.as_view(),
        name="sponsor-email-detail",
    ),
    url(
        r"^email/(?P<pk>\d+)/delete/$",
        view=SponsorEmailDeleteView.as_view(),
        name="sponsor-email-delete",
    ),
    url(
        r"^email/(?P<pk>\d+)/resend/$",
        view=SponsorEmailResendView.as_view(),
        name="sponsor-email-resend",
    ),
]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})
    ]
