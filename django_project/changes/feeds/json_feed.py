# coding=utf-8
import json

from django.utils.encoding import force_str as force_unicode
from django.utils.feedgenerator import SyndicationFeed, rfc2822_date


class JSONFeed(SyndicationFeed):
    content_type = "application/json; charset=utf-8"

    def write(self, outfile, encoding):
        data = {"rss": {"version": "2.0", "channel": self.add_root_elements()}}

        if self.items:

            item_element = []

            for item in self.items:
                item_element += [
                    self.add_item_elements(item),
                ]

            data["rss"]["channel"]["item"] = item_element

        outfile.write(json.dumps(data))

    def add_item_elements(self, item):
        item_elements = {
            "title": item["title"],
            "slug": item["slug"],
            "link": item["link"],
        }

        if item["description"] is not None:
            item_elements["description"] = item["description"]

        if item["pubdate"] is not None:
            item_elements["pubDate"] = rfc2822_date(item["pubdate"])
        if item["unique_id"] is not None:
            guid_attrs = {}
            if isinstance(item.get("unique_id_is_permalink"), bool):
                guid_attrs["isPermaLink"] = str(item["unique_id_is_permalink"]).lower()
            item_elements["guid"] = item["unique_id"]

        # Add image url attributes for member
        if item["image_url"] is not None:
            domain_url = self.feed["link"]
            head, sep, tail = domain_url.partition("/en/")
            item_elements["image_url"] = head + item["image_url"]
        # Add member_level
        if item["member_level"] is not None:
            item_elements["member_level"] = item["member_level"]
        # Country
        if item["member_country"] is not None:
            item_elements["member_country"] = force_unicode(item["member_country"])
        # Start date
        if item["start_date"] is not None:
            item_elements["start_date"] = item["start_date"]
        # End date
        if item["end_date"] is not None:
            item_elements["end_date"] = item["end_date"]
        # Member url
        if item["member_url"] is not None:
            item_elements["member_url"] = item["member_url"]
        return item_elements

    def add_root_elements(self):
        root_elements = {
            "title": self.feed["title"],
            "link": self.feed["link"],
            "description": self.feed["description"],
            "lastBuildDate": rfc2822_date(self.latest_post_date()),
        }

        return root_elements
