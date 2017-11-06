import sys
sys.path.insert(0, '/home/vinny_ricciardi/virtenvs/py2_api_rss_scrape/lib/python2.7/site-packages');

import feedparser
import pandas as pd
import urllib2
import os
import glob
import datetime as dt


# Function reads in rss feeds
def getRSS(path, path_2_rssout, path_2_cookies):

    df = pd.read_csv(path)
    df = df.loc[df['active'] == 1,
                ['site', 'rss_url', 'subdomain', 'cookies']]

    dictionary = dict(zip(df['rss_url'],
                      zip(df['site'], df['subdomain'], df['cookies'])))

    for k, v in dictionary.iteritems():

        # print '\n'*10, v[0], v[1], '\n'*10

        now = dt.datetime.now().date()
        cookie = path_2_cookies + v[2]
        fp = path_2_rssout + v[0] + '_' + v[1] + '_' + str(now)
        os.system("mkdir '{}'".format(fp))
        os.system("wget --load-cookies {} {} -P {}".format(cookie, k, fp))
        print '\n'*10, fp, '\n'*10

newsurls = getRSS('/home/vinny_ricciardi/Documents/Scripts/Python/Projects/API_Research/Projects/Scripts/News_Scraper/source_feeds.csv',
                  '/home/vinny_ricciardi/Documents/Scripts/Python/Projects/API_Research/Projects/Scripts/News_Scraper/rss/',
                  '/home/vinny_ricciardi/Documents/Scripts/Python/Projects/API_Research/Projects/Scripts/News_Scraper/cookies/')



# # Function to fetch the rss feed and return the parsed RSS
# def parseRSS(rss_url):


# 	response = urllib2.urlopen(rss_url)
# 	rss = response.read()


# 	return feedparser.parse(rss)


# # Function grabs the rss feed headlines (titles) and returns them as a list
# def getHeadlines(rss_url, how='title'):

#     headlines = []

#     feed = parseRSS(rss_url)
#     for newsitem in feed['items']:
#         headlines.append(newsitem[how])

#     return headlines

# # A list to hold all headlines
# allheadlines = []

# newsurls = getRSS('/home/vinny_ricciardi/Documents/Scripts/Python/Projects/API_Research/Projects/Scripts/News_Scraper/source_feeds.csv',
#                   '/home/vinny_ricciardi/Downloads/tmp/')


# # Iterate over the feed urls
# for key, url in newsurls.items():

#     # Call getHeadlines() and combine the returned headlines with allheadlines
#     allheadlines.extend(getHeadlines(url, how='links'))

# # Iterate over the allheadlines list and print each headline
# # for hl in allheadlines:
# #     print(hl)

