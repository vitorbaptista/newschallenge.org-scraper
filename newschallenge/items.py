# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EntryItem(scrapy.Item):
    author = scrapy.Field()
    author_url = scrapy.Field()
    author_description = scrapy.Field()

    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    short_description = scrapy.Field()
    one_sentence_description = scrapy.Field()
    need_description = scrapy.Field()
    progress_description = scrapy.Field()
    successful_outcome = scrapy.Field()
    team = scrapy.Field()
    location = scrapy.Field()
