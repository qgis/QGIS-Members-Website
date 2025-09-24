# coding=utf-8

__author__ = "Anita Hapsari <anita@kartoza.com>"
__date__ = "23/10/2017"

import datetime

from base.models.project import Project
from changes.feeds.json_feed import JSONFeed
from changes.models.sponsorship_period import SponsorshipPeriod
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed


# noinspection PyMethodMayBeStatic
class RssSponsorFeed(Feed):
    """RSS Feed class for sponsor."""

    def get_object(self, request, *args, **kwargs):
        """Return project object that matches the project_slug.

        :param request: The incoming HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: A project
        :rtype: Project

        :raises: Http404
        """
        self.years_limit = request.GET.get("years_limit", "")
        project_slug = "qgis"
        self.domain_path_url = request.build_absolute_uri(reverse("homepage"))
        return get_object_or_404(Project, slug=project_slug)

    def title(self, obj):
        """Return a title for the RSS.

        :param obj: A project
        :type obj: Project

        :returns: Title of the RSS Feed.
        :rtype: str
        """
        return "RSS Sustaining Members of %s Project" % obj.name

    def description(self, obj):
        """Return a description for the RSS.

        :param obj: A project
        :type obj: Project

        :returns: Description of the RSS Feed.
        :rtype: str
        """
        return "These are the current sustaining members " "of {} project.".format(
            obj.name
        )

    def link(self, obj):
        """Return the url of the latest sponsor.

        :param obj: Latest sponsor of a project
        :type obj: SponsorshipPeriod

        :returns: Url of the latest sponsor.
        :rtype: str
        """
        return reverse("homepage")

    def items(self, obj):
        """Return latest sponsors of the project.

        :param obj: A project
        :type obj: Project

        :returns: List of latest sponsor of a project
        :rtype: list
        """
        today = datetime.datetime.now().date()
        return SponsorshipPeriod.objects.filter(
            project=obj, end_date__gte=today
        ).order_by("-sponsorship_level__value", "-end_date")

    def item_title(self, item):
        """Return the title of the sponsor.

        :param item: Sponsorship period object of a project
        :type item: Sponsorship period

        :returns: name of the sponsor
        :rtype: str
        """
        return item.sponsor.name

    def item_description(self, item):
        """Return the description of the sponsor.

        :param item: Sponsorship period object of a project
        :type item: Sponsorship period

        :returns: description of the sponsor
        :rtype: str
        """
        level_class = str(item.sponsorship_level.name).lower()
        head, sep, tail = self.domain_path_url.partition("/en/")

        data = {
            "domain": head,
            "member_logo": item.sponsor.logo.url,
            "member_level": item.sponsorship_level,
            "start_date": item.start_date.strftime("%d %B %Y"),
            "end_date": item.end_date.strftime("%d %B %Y"),
            "currency": item.currency,
            "amount_contributed": item.amount_sponsored,
            "member_class": level_class,
        }

        descriptions = (
            "<div>"
            '<img class="member_img {member_class}" '
            'src="{domain}{member_logo}" width="300px"></div>'
            '<p class="member_body {member_class}">'
            "<span>Membership level: {member_level}</span><br/>"
            "<span>Membership period: {start_date} - {end_date}</span><br/>"
            "<span>Amount contributed: "
            "{currency} {amount_contributed}<span></p>".format(**data)
        )
        return descriptions

    # def item_extra_kwargs(self, item):
    #    return {'image_url': item.sponsor.logo.url}
    def item_extra_kwargs(self, item):
        return {
            "image_url": item.sponsor.logo.url,
            "member_level": item.sponsorship_level.name,
            "member_country": item.sponsor.country.name,
            # '%d %B %Y' => "16 March 2019"
            # '%Y%m%d'   => "20181012"
            "start_date": item.start_date.strftime("%Y%m%d"),
            "end_date": item.end_date.strftime("%d %B %Y"),
        }


class RssPastSponsorFeed(RssSponsorFeed):
    """RSS Feed class for past sponsors."""

    def description(self, obj):
        """Return a description for the RSS.

        :param obj: A project
        :type obj: Project

        :returns: Description of the RSS Feed.
        :rtype: str
        """
        return "These are the past sustaining " "members of %s project." % obj.name

    def items(self, obj):
        """Return past (former) sponsors of the project.

        :param obj: A project
        :type obj: Project

        :returns: List of past sponsor of a project
        :rtype: list
        """
        today = datetime.datetime.now().date()
        try:
            self.years_limit = int(self.years_limit)
            if self.years_limit > 0:
                date_limit = today - datetime.timedelta(365 * self.years_limit)
                return SponsorshipPeriod.objects.filter(
                    project=obj, end_date__lt=today, end_date__gt=date_limit
                ).order_by("-end_date")
            else:
                return SponsorshipPeriod.objects.filter(
                    project=obj, end_date__lt=today
                ).order_by("-end_date")
        except ValueError:
            return SponsorshipPeriod.objects.filter(
                project=obj, end_date__lt=today
            ).order_by("-end_date")


class AtomSponsorFeed(RssSponsorFeed):
    """Atom Feed class for sponsor."""

    feed_type = Atom1Feed
    subtitle = RssSponsorFeed.description


class AtomPastSponsorFeed(RssPastSponsorFeed):
    """Atom Feed class for past sponsor."""

    feed_type = Atom1Feed
    subtitle = RssPastSponsorFeed.description


class JSONSponsorFeed(Feed):
    """JSON Feed class for sponsor."""

    feed_type = JSONFeed

    def get_object(self, request, *args, **kwargs):
        """Return project object that matches the project_slug.

        :param request: The incoming HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: A project
        :rtype: Project

        :raises: Http404
        """
        self.years_limit = request.GET.get("years_limit", "")
        project_slug = "qgis"
        self.domain_path_url = request.build_absolute_uri(reverse("homepage"))
        return get_object_or_404(Project, slug=project_slug)

    def title(self, obj):
        """Return a title for the RSS.

        :param obj: A project
        :type obj: Project

        :returns: Title of the RSS Feed.
        :rtype: str
        """
        return "JSON Sustaining Members of %s Project" % obj.name

    def description(self, obj):
        """Return a description for the RSS.

        :param obj: A project
        :type obj: Project

        :returns: Description of the RSS Feed.
        :rtype: str
        """
        return "These are the currrent sustaining members " "of {} project.".format(
            obj.name
        )

    def link(self, obj):
        """Return the url of the latest sponsor.

        :param obj: Latest sponsor of a project
        :type obj: SponsorshipPeriod

        :returns: Url of the latest sponsor.
        :rtype: str
        """
        return reverse("homepage")

    def items(self, obj):
        """Return latest sponsors of the project.
        NOT

        :param obj: A project
        :type obj: Project

        :returns: List of latest sponsor of a project
        :rtype: list
        """
        today = datetime.datetime.now().date()
        return SponsorshipPeriod.objects.filter(
            project=obj, end_date__gte=today
        ).order_by("-sponsorship_level__value", "-start_date")

    def item_title(self, item):
        """Return the title of the sponsor.

        :param item: Sponsorship period object of a project
        :type item: Sponsorship period

        :returns: name of the sponsor
        :rtype: str
        """
        return item.sponsor.name

    def item_description(self, item):
        """Return the description of the sponsor.

        :param item: Sponsorship period object of a project
        :type item: Sponsorship period

        :returns: description of the sponsor
        :rtype: str
        """
        return ""

    def item_extra_kwargs(self, item):
        return {
            "slug": item.sponsor.slug,
            "image_url": item.sponsor.logo.url,
            "member_level": item.sponsorship_level.name,
            "member_country": item.sponsor.country.name,
            "member_url": item.sponsor.sponsor_url,
            # '%d %B %Y' => "16 March 2019"
            # '%Y%m%d'   => "20181012"
            "start_date": item.start_date.strftime("%d %B %Y"),
            "end_date": item.end_date.strftime("%d %B %Y"),
        }


class JSONPastSponsorFeed(JSONSponsorFeed):
    """JSON Feed class for past sponsor."""

    def description(self, obj):
        """Return a description for the RSS.

        :param obj: A project
        :type obj: Project

        :returns: Description of the RSS Feed.
        :rtype: str
        """
        return "These are the past sustaining members " "of %s project." % obj.name

    def items(self, obj):
        """Return past (former) sponsors of the project.

        :param obj: A project
        :type obj: Project

        :returns: List of past sponsor of a project
        :rtype: list
        """
        today = datetime.datetime.now().date()
        try:
            self.years_limit = int(self.years_limit)
            if self.years_limit > 0:
                date_limit = today - datetime.timedelta(365 * self.years_limit)
                return SponsorshipPeriod.objects.filter(
                    project=obj, end_date__lt=today, end_date__gt=date_limit
                ).order_by("-end_date")
            else:
                return SponsorshipPeriod.objects.filter(
                    project=obj, end_date__lt=today
                ).order_by("-end_date")
        except ValueError:
            return SponsorshipPeriod.objects.filter(
                project=obj, end_date__lt=today
            ).order_by("-end_date")
