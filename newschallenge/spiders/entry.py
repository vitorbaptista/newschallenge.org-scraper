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
        clean = lambda selector: self._clean(selector)

        entry = newschallenge.items.EntryItem()

        entry["url"] = response.url

        author_box = response.css(".author-box-big")
        entry["author"] = clean(author_box.css(".name::text")[0])
        author_url = clean(author_box.css("a[itemprop='url']::attr('href')")[0])
        entry["author_url"] = response.urljoin(author_url)
        author_description = author_box.css("[itemprop='description']")
        if author_description:
            entry["author_description"] = clean(author_description[0])

        entry["title"] = clean(response.css("[itemprop='name headline']::text")[0])
        entry["short_description"] = clean(response.css("[itemprop='description']::text")[0])
        entry["description"] = clean(response.css("[itemprop='articleBody'] *")[0])

        for text_field in response.css("section.primary-text"):
            field = self._get_field_name(text_field)
            entry[field] = self._get_field_text(text_field)

        return entry

    def _get_field_name(self, selector):
        FIELDS = {
            "In one sentence, describe your idea as simply as possible.": "one_sentence_description",
            "Briefly describe the need that you're trying to address.": "need_description",
            "What progress have you made so far?": "progress_description",
            "What would be a successful outcome for your project?": "successful_outcome",
            "Please list your team members and their relevant experience/skills.": "team",
            "Location": "location",
        }
        headline = selector.css(".sub-headline-text::text")
        if headline:
            return FIELDS[headline[0].extract().strip()]

    def _get_field_text(self, selector):
        text = selector.extract().strip()
        start_index = text.find("</h1>")
        end_index = text.rfind("</section>")

        if start_index != -1 and end_index != -1:
            start_index_offset = len("</h1>")
            return text[(start_index + start_index_offset):end_index].strip()

    def _clean(self, selector):
        return selector.extract().strip()
