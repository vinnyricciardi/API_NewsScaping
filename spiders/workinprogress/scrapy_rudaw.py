#!/usr/bin/env python3
import scrapy
import pandas as pd


class BrickSetSpider(scrapy.Spider):

	name = 'rudaw_spider'
	start_urls = ['http://www.rudaw.net/SearchArchive.aspx?PageID=15813&cat=531']


	def __init__(self):
		
		self.out = pd.DataFrame(columns=['date', 'title', 'description', 'url'])
		self.dates = []
		self.titles = []
		self.descrips = []
		self.urls = []


	def parse(self, response):

		SET_SELECTOR = '.topStoryItem'

		# We define our link to the next page
		NEXT_PAGE_SELECTOR = "//div[@class='rgWrap']/@href"
		# # We extract the link using xpath
		next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
		print('\n\n\n')
		print(next_page)
		print('\n\n\n')
		# for news in response.css(SET_SELECTOR):
		# 	print('\n\n\n\n\n\n')
		# 	print('\n\n\n\n\n\n')

		# 	DATE_SELECTOR = "//span[@class='newsDate']/@text"
		# 	TITLE_SELECTOR = 'h1 span ::text'
		# 	DESCRIP_SELECTOR = 'table td ::text'
		# 	URL_SELECTOR = 'h1 a ::attr(href)'

		# 	self.dates.append(news.xpath(DATE_SELECTOR).extract())
		# 	self.titles.append(news.css(TITLE_SELECTOR).extract())
		# 	self.descrips.append(news.css(DESCRIP_SELECTOR).extract())
		# 	self.urls.append(news.css(URL_SELECTOR).extract())

		# 	print('\n\n\n\n\n\n')
		# 	print(news.xpath(DATE_SELECTOR).extract())
		# 	print('\n\n\n\n\n\n')

		# out2 = pd.DataFrame(columns=['date', 'title', 'description', 'url'])

		# out2['date'] = self.dates
		# out2['title'] = self.titles
		# out2['description'] = self.descrips
		# out2['url'] = self.urls


		# for c in out2.columns:
		# 	out2[c] = out2[c].str.encode('utf-8')

		# self.out = pd.concat([self.out, out2], axis=0)
		# print('\n\n\n\n\n\n')
		# print(len(self.out))
		# print('\n\n\n\n\n\n')


		# 		# We put a conditional if there is a next page url then rerun the parser
		# if next_page:
		# 	yield scrapy.Request(
		# 		response.urljoin(next_page),
		# 		callback=self.parse
		# 	)

		# request the next page
		# data = {
		#     '__EVENTARGUMENT': 'Page$%d' % current_page,
		#     '__EVENTVALIDATION': re.search(r"__EVENTVALIDATION\|(.*?)\|", response.body, re.MULTILINE).group(1),
		#     '__VIEWSTATE': re.search(r"__VIEWSTATE\|(.*?)\|", response.body, re.MULTILINE).group(1),
		#     '__ASYNCPOST': 'true',
		#     '__EVENTTARGET': 'ctl00$phTwoColumns$phMain$gvNodes$ctl00$ctl03$ctl01$ctl{}'.format(),
		#     'ctl00$MainContent$ScriptManager1': 'ctl00$MainContent$UpdatePanel1|ctl00$MainContent$agentList',
		#     '': ''
		# }

		# return FormRequest(url=URL,
		#                    method='POST',
		#                    formdata=data,
		#                    callback=self.parse_page,
		#                    meta={'page': current_page},
		#                    dont_filter=True,
		#                    headers=HEADERS)

		# else:
		# 	self.out.loc[:, ['date', 'title', 'description', 'url']]
		# 	self.out = self.out.drop_duplicates()
		# 	self.out.to_csv('data/ekurd_spider_02042018.csv')
