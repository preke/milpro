# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MilproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    readnum = scrapy.Field()
    commentNum = scrapy.Field()
    isHandled = scrapy.Field()
    keywords = scrapy.Field()
    abstract = scrapy.Field()
    event = scrapy.Field()
