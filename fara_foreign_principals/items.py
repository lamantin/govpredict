# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FaraForeignPrincipalJsOnItem(scrapy.Item):
    
    url = scrapy.Field()
    country = scrapy.Field()
    state = scrapy.Field()
    reg_num = scrapy.Field()
    address = scrapy.Field()
    foreign_principal = scrapy.Field()
    date = scrapy.Field()
    registrant = scrapy.Field()
    exhibit_url = scrapy.Field()

    def process_item(self, item, spider):
        return item
