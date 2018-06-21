#!/usr/bin/env python3
import scrapy
import pandas as pd
import datetime as dt


class NewsSpider(scrapy.Spider):

	name = 'newsspider'
	start_urls = ['http://ekurd.net/all-news']


	def __init__(self):
		
		self.out = pd.DataFrame(columns=[
			'Date', 
			'Title', 
			'Description', 
			'URL', 
			'Domain',
			'SubDomain',
			'DownloadDate',
			'Type'])
		self.dates = []
		self.titles = []
		self.descrips = []
		self.urls = []
		self.domain = []
		self.subdomain = []
		self.downloadate = []
		self.type = []
		self.now = str(dt.datetime.now().date())


	def parse(self, response):

		SET_SELECTOR = '.entry-list'

		# Define the link to the next page
		NEXT_PAGE_SELECTOR = "//a[@class='nextpostslink']/@href"
		# Extract the link using xpath
		next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
		
		for news in response.css(SET_SELECTOR):

			DATE_SELECTOR = 'aside a time::text'
			TITLE_SELECTOR = 'h2 a ::text'
			DESCRIP_SELECTOR = 'p ::text'
			URL_SELECTOR = 'h2 a ::attr(href)'

			self.dates.append(news.css(DATE_SELECTOR).extract()[0])
			self.titles.append(news.css(TITLE_SELECTOR).extract()[0])
			self.descrips.append(news.css(DESCRIP_SELECTOR).extract()[0])
			self.urls.append(news.css(URL_SELECTOR).extract()[0])
			self.domain.append('ekurd')
			self.subdomain.append('all')
			self.downloadate.append(self.now)
			self.type.append('archive')

			print('ekurd', 'all')
			print('----', news.css(DATE_SELECTOR).extract()[0])

		out2 = pd.DataFrame(columns=[
			'Date', 
			'Title', 
			'Description', 
			'URL', 
			'Domain',
			'SubDomain',
			'DownloadDate',
			'Type'])

		out2['Date'] = self.dates
		out2['Title'] = self.titles
		out2['Description'] = self.descrips
		out2['URL'] = self.urls
		out2['Domain'] = self.urls
		out2['SubDomain'] = self.urls
		out2['DownloadDate'] = self.urls
		out2['Type'] = self.urls

		for c in out2.columns:
			out2[c] = out2[c].str.encode('utf-8')

		self.out = pd.concat([self.out, out2], axis=0)

		# Put a conditional if there is a next page url then rerun the parser
		if next_page:
			yield scrapy.Request(
				response.urljoin(next_page),
				callback=self.parse
			)

		else:
			self.out.loc[:, [
			'Date', 
			'Title', 
			'Description', 
			'URL', 
			'Domain',
			'SubDomain',
			'DownloadDate',
			'Type']]
			self.out = self.out.drop_duplicates()
			self.out.to_csv('../data/ekurd_spider_{}.csv'.format(self.now))
