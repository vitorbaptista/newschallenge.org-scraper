# -*- coding: utf-8 -*-

import scrapy

import newschallenge.items


class EntrySpider(scrapy.spiders.Spider):
    name = "entry"
    allowed_domains = ["newschallenge.org"]
    start_urls = [
        "https://www.newschallenge.org/challenge/data/entries",
    ]

    def parse(self, response):
        for href in response.css(".contribution-list figure a::attr('href')"):
            entry_url = response.urljoin(href.extract())
            yield scrapy.Request(entry_url, callback=self._parse_entry)

        next_page_href = response.css(".contribution-paginator a.active + a::attr('href')")
        if next_page_href:
            next_page_url = response.urljoin(next_page_href[0].extract())
            yield scrapy.Request(next_page_url)

    def _parse_entry(self, response):
        clean = lambda selector: selector.extract().strip()

        entry = newschallenge.items.EntryItem()

        entry["title"] = clean(response.css("[itemprop='name headline']::text")[0])
        entry["description"] = clean(response.css("[itemprop='description']::text")[0])

        author_box = response.css(".author-box-big")
        entry["author"] = clean(author_box.css(".name::text")[0])
        author_url = clean(author_box.css("a[itemprop='url']::attr('href')")[0])
        entry["author_url"] = response.urljoin(author_url)
        entry["author_description"] = clean(author_box.css("[itemprop='description']")[0])

        return entry
