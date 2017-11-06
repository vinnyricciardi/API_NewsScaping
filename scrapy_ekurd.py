#!/usr/bin/env python3
import scrapy
import pandas as pd


class BrickSetSpider(scrapy.Spider):

    name = 'ekurd_spider'
    start_urls = ['http://ekurd.net/all-news']


    def __init__(self):
    
        self.out = pd.DataFrame(columns=['date', 'title', 'description', 'url'])
        self.dates = []
        self.titles = []
        self.descrips = []
        self.urls = []


    def parse(self, response):

        SET_SELECTOR = '.entry-list'

        NEXT_PAGE_SELECTOR = "//a[@class='nextpostslink']/@href"
        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()

        for news in response.css(SET_SELECTOR):

            DATE_SELECTOR = 'aside a time::text'
            TITLE_SELECTOR = 'h2 a ::text'
            DESCRIP_SELECTOR = 'p ::text'
            URL_SELECTOR = 'h2 a ::attr(href)'

            self.dates.append(news.css(DATE_SELECTOR).extract())
            self.titles.append(news.css(TITLE_SELECTOR).extract())
            self.descrips.append(news.css(DESCRIP_SELECTOR).extract_first())
            self.urls.append(news.css(URL_SELECTOR).extract())

        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

        out2 = pd.DataFrame(columns=['date', 'title', 'description', 'url'])

        out2['date'] = self.dates
        out2['title'] = self.titles
        out2['description'] = self.descrips
        out2['url'] = self.urls

        for c in out2.columns:
            out2[c] = out2[c].astype(str)

        self.out = pd.concat([self.out, out2], axis=0)
        self.out.to_csv('~/Downloads/test.csv')
