# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class NewsItem(Item):
    # 新闻标题、链接、正文、发布时间、来源、站点名称
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    url = Field()
    text = Field()
    datetime = Field()
    source = Field()
    website = Field()

