#!/usr/bin/env python3
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

        now = dt.datetime.now().date()
        cookie = path_2_cookies + v[2]
        fp = path_2_rssout + v[0] + '_' + v[1] + '_' + str(now)
        os.system("mkdir '{}'".format(fp))
        os.system("wget --load-cookies {} {} -P {}".format(cookie, k, fp))

newsurls = getRSS('/home/vinny_ricciardi/Documents/Scripts/Python/Projects/API_Research/Projects/Scripts/News_Scraper/source_feeds.csv',
                  # '/home/vinny_ricciardi/Documents/Scripts/Python/Projects/API_Research/Projects/Scripts/News_Scraper/rss/',
                  '/home/vinny_ricciardi/Documents/Data_Library_SSD/Webscraping/APInewsScraper/rss/',
                  '/home/vinny_ricciardi/Documents/Scripts/Python/Projects/API_Research/Projects/Scripts/News_Scraper/cookies/')

