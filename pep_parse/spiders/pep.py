import re

import scrapy


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('a[href^="pep"]')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        text = response.css('h1.page-title::text').get()
        match = re.search(r"PEP (\d+)\s*–\s*(.+)", text)
        yield {
            'number': match.group(1),
            'name': match.group(2),
            'status': response.css('abbr::text').get()
        }
