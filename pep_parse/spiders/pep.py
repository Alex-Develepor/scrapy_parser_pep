import scrapy
from scrapy import Selector

from pep_parse.constants import PATTERN
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_info: Selector = response.css(
            "section[id='numerical-index']"
        ).css("tbody")[0]
        links = pep_info.css("a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_info = response.css("section[id='pep-content']")
        h1_title = PATTERN.search(pep_info.css("h1::text").get())
        status = pep_info.css("abbr::text").get()
        if h1_title:
            number, name = h1_title.group("number", "name")
            data = {
                "number": number,
                "name": name,
                "status": status
            }
            yield PepParseItem(data)
