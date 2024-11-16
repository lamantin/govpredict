from __future__ import absolute_import
# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from fara_foreign_principals.items import FaraForeignPrincipalJsOnItem
from urlparse import urlparse
from datetime import datetime

class CleanSpider(scrapy.Spider):
    name = "clean"
    keyword = 'Active Foreign Principals'
    allowed_domains = ["www.fara.gov"]
    resulttable_class = 'apexir_WORKSHEET_DATA'
    start_urls = [
        'https://www.fara.gov/quick-search.html',
    ]
    queryoptionselector = "P130_CNTRY"
    extended_url = 'https://efile.fara.gov/pls/apex/'
    instance_id = False
    switcher_url = False

    def __init__(self, category=None, *args, **kwargs):
        self.item = None
        super(CleanSpider, self).__init__(*args, **kwargs)

    def prepare_request_querystring(self, url):

        parsed = urlparse(url)
        qs = parsed.query
        q1 = qs.split("=")[1].split(',')[0].split('::')[0][:-1]
        return ''.join([parsed.scheme, '://', parsed.netloc, parsed.path,'?p=', q1, self.actual_placeholder, self.queryoptionselector, ':'])

    def a_placeholder(self,selects):
        return selects.split('+')[0].replace("location.href='f?p=171:130:", '').replace(self.queryoptionselector, '').replace("'", "")[:-1]    

    def start_requests(self):

        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.getIframe
        )

    def getIframe(self, response):
        hxs = Selector(response)
        iframe = hxs.xpath('//iframe/@src')
        new_url = iframe.extract()[0]
        yield self.make_requests_from_url(new_url).replace(callback=self.choose_foreign_principals)

    def choose_foreign_principals(self, response):

        hxs = Selector(response)
        elems = hxs.xpath("//a[@href]")
        new_url = str(self.extended_url) +str(elems[18].xpath('@href').extract()[0].encode('utf-8'))
        yield self.make_requests_from_url(new_url).replace(callback=self.work_inframe)

    

        
    def work_inframe(self, response):
        hxs = Selector(response)
        selects = hxs.xpath("//select[@id='" + self.queryoptionselector + "']/@onchange").extract()[0].encode('utf-8')

        self.actual_placeholder = self.a_placeholder(selects)
        for country_code in hxs.xpath("//select[@id='" + self.queryoptionselector + "']/option/@value").extract():
            if country_code != 'ALL':
                yield self.make_requests_from_url(''.join([self.prepare_request_querystring(response.url), country_code.encode('utf-8')])).replace(callback=self.parse_country_landing)

    def exhibit_url(self,response):

         nxs = Selector(response)
         
         try:
            exhibit_url = nxs.xpath("//table[@class='" + self.resulttable_class + "']//tr/td/a//@href").extract()[0].encode('utf-8')
         except:   
            exhibit_url = None   
         
         self.item['exhibit_url'] = exhibit_url
         yield self.item

    def parse_country_landing(self, response):
        nxs = Selector(response)
        actual_country = nxs.xpath("//select/option[@selected='selected']/text()").extract()[
            0].encode('utf-8').lower().capitalize()
        rows = nxs.xpath(
            "//table[@class='" + self.resulttable_class + "']//tr")
        for row in rows:
            try:
                hclass = row.xpath('@class').extract()[0].encode('utf-8')
            except IndexError:
                hclass = False
            if hclass != False:
                if hclass in ['odd', 'even']:
                    line = row.css('tr')
                    
                    for l in line:

                        try:
                            url =  self.extended_url+str(l.xpath("//tr[@class='"+hclass+"']/td[contains(@headers,'LINK')]/a/@href").extract()[0].encode('utf-8'))
                        
                        except:
                            url = None
                        try:
                            country = actual_country
                        except:
                            country = None

                        try:
                            state = l.xpath("//tr[@class='"+hclass+"']/td[contains(@headers,'STATE')]/text()").extract()[0].encode('utf-8')
                        except:
                            state = None 

                        try:
                            reg_num = l.xpath("//tr[@class='"+hclass+"']/td[contains(@headers,'REG_NUMBER')]/text()").extract()[0].encode('utf-8')
                        except:
                            reg_num = None             

                        try:
                            address = l.xpath("//tr[@class='"+hclass+"']/td[contains(@headers,'ADDRESS_1')]/text()").extract()[0].encode('utf-8')
                        except:
                            address = None

                        try:
                            foreign_principal = l.xpath("//tr[@class='"+hclass+"']/td[contains(@headers,'FP_NAME')]/text()").extract()[0].encode('utf-8')
                        except:
                            foreign_principal = None
        
                        try:
                            date = l.xpath("//tr[@class='"+hclass+"']/td[contains(@headers,'REG_DATE')]/text()").extract()[0].encode('utf-8')
                            #07/03/2013
                            date = datetime.strptime(date, '%m/%d/%Y')
                            date = date.isoformat()
                        except:
                            date = None

                        try:
                            registrant = l.xpath("//tr[@class='"+hclass+"']/td[contains(@headers,'REGISTRANT_NAME')]/text()").extract()[0].encode('utf-8')
                        except:
                            registrant = None
        
                        

                        exhibit_url = None                              
                        self.item = FaraForeignPrincipalJsOnItem(url=url,country=country,state=state,reg_num=reg_num,address=address,foreign_principal=foreign_principal,date=date,registrant=registrant,exhibit_url=exhibit_url)
                        yield self.make_requests_from_url(self.extended_url + str(l.xpath('//td//a/@href').extract()[-1])).replace(callback=self.exhibit_url)
                                
