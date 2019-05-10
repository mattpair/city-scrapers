import re
from datetime import datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class ChiSouthwestHomeEquityIlSpider(CityScrapersSpider):
    name = "chi_southwest_home_equity_il"
    agency = "Chicago Southwest Home Equity Commission I"
    timezone = "America/Chicago"
    allowed_domains = ["swhomeequity.com"]
    start_urls = ["https://swhomeequity.com/agenda-%26-minutes"]
    TAG_RE = re.compile(r'<[^>]+>')

    def parse(self, response):

        table = response.xpath('//*[@id="01b1278e-65d6-45f0-a295-b24aefce85b6"]/div/div/section/div/div[2]')

        for item in response.css(".meetings"):
            meeting = Meeting(
                title=self._parse_title(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                all_day=False,
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        return "Board Meeting"

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return BOARD

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return None

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "5334 W. 65th Street, Chicago, IL 60638",
            "name": "Southwest Home Equity Assurance Office",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url

    def _clean_html_tags(self, item):
        return self.TAG_RE.sub('', item).strip()
