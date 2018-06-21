#!/usr/bin/env python3
import scrapy
import pandas as pd
import datetime as dt


class NewsSpider(scrapy.Spider):

	name = 'newsspider'
	start_urls = ['https://english.alarabiya.net/News/gulf/archive.news.html']

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

		SET_SELECTOR = '.detail'
		
		# We define our link to the next page
		NEXT_PAGE_SELECTOR = "//a[@class='next']/@href"
		# We extract the link using xpath
		next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()

		for news in response.css(SET_SELECTOR):

			DATE_SELECTOR = 'p ::text'
			TITLE_SELECTOR = 'a ::text'
			DESCRIP_SELECTOR = DATE_SELECTOR
			URL_SELECTOR = 'a ::attr(href)'

			self.dates.append(news.css(DATE_SELECTOR).extract()[0])
			self.titles.append(news.css(TITLE_SELECTOR).extract()[0])
			self.descrips.append(news.css(DESCRIP_SELECTOR).extract()[1])
			self.urls.append(news.css(URL_SELECTOR).extract()[0])
			self.domain.append('alarabiya')
			self.subdomain.append('gulf')
			self.downloadate.append(self.now)
			self.type.append('archive')

			print('alarabiya', 'gulf')
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
		out2['Domain'] = self.domain
		out2['SubDomain'] = self.subdomain
		out2['DownloadDate'] = self.downloadate
		out2['Type'] = self.type

		for c in out2.columns:
			out2[c] = out2[c].str.encode('utf-8')

		self.out = pd.concat([self.out, out2], axis=0)

		# We put a conditional if there is a next page url then rerun the parser
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
			self.out.to_csv('../data/alarabiya_gulf_{}.csv'.format(self.now))
