# -*- coding: utf-8 -*-
import os

import scrapy
from home_uk import settings


class HomeUKSpider(scrapy.Spider):
    name = 'home_uk'
    allowed_domains = ['worldpostalcode.com', 'home.co.uk']
    start_urls = []

    search_url = 'https://worldpostalcode.com/search/'
    extract_url = 'https://www.home.co.uk/guides/asking_prices_report.htm?location={post_code}&all=1'

    def __init__(self, name=None, **kwargs):
        # Load seller
        super(HomeUKSpider, self).__init__(name, **kwargs)
        city_file = getattr(settings, 'CITY_FILE', None)
        if city_file and os.path.exists(city_file):
            cities = []
            for line in open(city_file):
                if "#" not in line:
                    cities.append(line.strip("\n"))
            self.cities = list(filter(None, cities))
        else:
            raise Exception('NOT FOUND CITY_FILE!')

    def start_requests(self):
        export_path = '%s/%s' % (os.path.dirname(__file__), 'cities1.txt')

        for i, city in enumerate(self.cities):
            if i < 2600 : continue
            # if i > 2700 : break
            data = {"val": city}
            print('Start: %s' % city)
            # yield scrapy.Request('https://worldpostalcode.com/united-kingdom/england/'+city.strip().replace(' ', '-'), callback=self.parse, meta={'city': city})
            url = self.extract_url.format(post_code=city.lower())
            yield scrapy.Request(url, callback=self.extract_result, meta={'data': city})
    def parse(self, response):
        city = response.meta.get('city')

        # trs = response.xpath('//table/tr')
        # data = []
        # if not trs:
        #     raise Exception('NOT FOUND POSTAL CODE!')
        # for tr in trs:
        #     td = tr.xpath('.//td')
        #     if td:
        #
        #         raw = td[3].xpath('.//text()').extract_first(default='').strip()
        #         # some code have multi value
        #         codes = raw.split(',')
        #         for code in codes:
        #             code = code.strip()
        #             d = {
        #                 'city': city,
        #                 'location': td[2].xpath('.//text()').extract_first(default=''),
        #                 'code': code
        #             }
        #             if not any(d['code'] == code for d in data):
        #                 data.append(d)
        divs = response.xpath('//div[@class="unit"]')
        data = []

        for di in divs:
            location = di.xpath('./div[@class="place"]/text()').extract_first()
            codes = di.xpath('./div[@class="code"]/span/text()').extract()
            for code in codes:
                code = code.strip()
                d = {
                    'city': city,
                    'location': location,
                    'code': code
                }
                if not any(d['code'] == code for d in data):
                    data.append(d)
        if not data:
            raise Exception('NOT FOUND POSTAL CODE!')

        for p in data:
            url = self.extract_url.format(post_code=p['code'].lower())
            yield scrapy.Request(url, callback=self.extract_result, meta={'data': p})

    def extract_result(self, response):
        data = response.meta.get('data', {})
        by_type_tr = response.xpath('//h2[contains(., "Median Property Asking Prices By Type")]/following-sibling::table[1]/tr')
        by_number_tr = response.xpath('//h2[contains(., "Median Property Asking Prices By Number of Bedrooms")]/following-sibling::table[1]/tr')

        by_type_data = {}
        by_number_data = {}
        type_start = 'Start date'
        type_end = 'End date'

        if not by_type_tr:
            pass

        for i, tr in enumerate(by_type_tr):
            td = tr.xpath('.//td')
            if i == 0:
                type_start = td[1].xpath('.//text()').extract_first(default='').strip()
                type_end = td[2].xpath('.//text()').extract_first(default='').strip()
            else:
                name = td[2].xpath('.//text()').extract_first(default='').strip()
                by_type_data[name] = {
                    '_StartTime': type_start,
                    '_EndTime': type_end,
                    'StartTime': td[3].xpath('.//text()').extract_first(default='').strip(),
                    'EndTime': td[4].xpath('.//text()').extract_first(default='').strip(),
                    'Change': td[5].xpath('.//text()').extract_first(default='').strip(),
                }

        # Extract by_number_data
        for i, tr in enumerate(by_number_tr):
            td = tr.xpath('.//td')
            if i == 0:
                type_start = td[1].xpath('.//text()').extract_first(default='').strip()
                type_end = td[2].xpath('.//text()').extract_first(default='').strip()
            else:
                name = td[2].xpath('.//text()').extract_first(default='').strip()
                by_number_data[name] = {
                    '_StartTime': type_start,
                    '_EndTime': type_end,
                    'StartTime': td[3].xpath('.//text()').extract_first(default='').strip(),
                    'EndTime': td[4].xpath('.//text()').extract_first(default='').strip(),
                    'Change': td[5].xpath('.//text()').extract_first(default='').strip(),
                }

        # Response data
        # Ignore empty data
        if by_type_data:
            for key, value in by_type_data.iteritems():

                item = {
                    # 'Location': data['location'],
                    #     'City': data['city'],
                        'Code': data,
                        'chart': 'type'}
                value['Type'] = key
                item.update(value)
                yield item
        if by_number_data:
            for key, value in by_number_data.iteritems():
                item = {
                    # 'Location': data['location'],
                    #     'City': data['city'],
                        'Code': data,
                        'chart': 'number'}
                value['Type'] = key
                item.update(value)
                yield item


