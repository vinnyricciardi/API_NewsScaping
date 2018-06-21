import json
import scrapy
import pandas as pd
 

class NewsSpider(scrapy.Spider):
    name = 'newsspider'
    base_url = 'http://www.kurdistan24.net/page/LoadMorePaggingData?hdnSelectedPageId={}&settingModelstr=%7B%26quot%3BchkThumbShow%26quot%3B%3Afalse%2C%26quot%3BchkDisplayTitle%26quot%3B%3Atrue%2C%26quot%3BchkDisplaySubTitle%26quot%3B%3Atrue%2C%26quot%3BchkFeatured%26quot%3B%3Afalse%2C%26quot%3BchkDisplayVisitDetails%26quot%3B%3Afalse%2C%26quot%3BchkSlidShow%26quot%3B%3Afalse%2C%26quot%3BchkTopStory%26quot%3B%3Afalse%2C%26quot%3BchkHightLight%26quot%3B%3Afalse%2C%26quot%3BchkAnimationAutoPlay%26quot%3B%3Afalse%2C%26quot%3Bcategoryid%26quot%3B%3A%26quot%3B367%26quot%3B%2C%26quot%3BPersonId%26quot%3B%3Anull%2C%26quot%3BarticleTypeId%26quot%3B%3A%26quot%3B0%26quot%3B%2C%26quot%3BpageId%26quot%3B%3A%26quot%3B809%26quot%3B%2C%26quot%3BcbxType%26quot%3B%3A%26quot%3B1%26quot%3B%2C%26quot%3BcbxColsm%26quot%3B%3A%26quot%3B6%26quot%3B%2C%26quot%3BtxtDisplayCount%26quot%3B%3A%26quot%3B200%26quot%3B%2C%26quot%3BtxtPaggingOfter%26quot%3B%3Anull%2C%26quot%3BtxtNewsOf%26quot%3B%3A%26quot%3B0%26quot%3B%2C%26quot%3BtxtSkipCount%26quot%3B%3A%26quot%3B16%26quot%3B%2C%26quot%3BtxtGroupBy%26quot%3B%3A%26quot%3B1%26quot%3B%2C%26quot%3BtxtViewPath%26quot%3B%3Anull%7D&tag='
    page = 1
    start_urls = [base_url.format(page)]
    download_delay = 1.5

    def __init__(self):
    
        self.out = pd.DataFrame(columns=['date', 'title', 'description', 'url'])
        self.dates = []
        self.titles = []
        self.descrips = []
        self.urls = []
        self.page_number = 1  # Current workaround for iterating through pages
 
    def parse(self, response):

        SET_SELECTOR = '.ArchiveList .no-gutter'

        i = 0
        for news in response.css(SET_SELECTOR):

            DATE_SELECTOR = 'a h5 ::text'
            TITLE_SELECTOR = 'a h4 ::text'
            DESCRIP_SELECTOR = 'a p ::text'
            URL_SELECTOR = "//@href"

            self.dates.append(news.css(DATE_SELECTOR).extract()[0])
            self.titles.append(news.css(TITLE_SELECTOR).extract()[0])
            self.descrips.append(news.css(DESCRIP_SELECTOR).extract()[0])
            self.urls.append('http://www.kurdistan24.net/en' + news.xpath(URL_SELECTOR).extract()[i][3:])
            i += 1

        out2 = pd.DataFrame(columns=['date', 'title', 'description', 'url'])

        out2['date'] = self.dates
        out2['title'] = self.titles
        out2['description'] = self.descrips
        out2['url'] = self.urls

        for c in out2.columns:
            out2[c] = out2[c].astype(str)

        self.out = pd.concat([self.out, out2], axis=0)

        # We put a conditional if there is a next page url then rerun the parser
        # In this case it's a page that loads more content as we scroll down
        # Each time we scroll, the page makes an ajax request using a new PageId
        # in the base_url we defined
        
        # TODO: This loop currently is manually set for the number of pages to scrape, 
        # should figure out a better if statement to request all the pages in the database.

        if self.page_number < 300:  # Can set 300 to any number. This represents the number of pages we want to scrape.

            self.page_number += 1
            # Note, redfining base_url as a local variable because there was a bug when assigning via self method,
            # not great form, but workable

            next_page = self.base_url.format(self.page_number)

            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
    
        else:
    
            self.out = self.out.drop_duplicates()  # Had an issue with capturing duplicates each time new ajax request made. Simple, inelagant solution.
            self.out.to_csv('data/kurdistan24_02022018.csv')
