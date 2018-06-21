#/usr/bin/python3.6
import feedparser
import pandas as pd
import os
import fnmatch
import glob


# Traverse rss directories and capture desired feeds
base_dir = '../rss/'
pattern = ['ekurd', 'alarabiya', 'almonitor', 'aljazeera']
columns = [
    'Date', 
    'Title', 
    'Description', 
    'URL', 
    'Domain',
    'SubDomain',
    'DownloadDate',
    'Type']

df = pd.DataFrame(columns=columns)

direcs = os.listdir(base_dir)

for direc in direcs:

    if any(xs in direc for xs in pattern):
        
        path = base_dir + direc
        try:
            file = glob.glob(path + '/*')[0]
            print(file)
        
            d = feedparser.parse(file)

            date_ = []
            title_ = []
            descr_ = []
            url_ = []
            domain_ = []
            subdomain_ = []
            downloaddate_ = []
            type_ = []

            for post in d.entries:

                date_.append(post.published)
                title_.append(post.title)
                descr_.append(post.description)
                url_.append(post.link)
                s = direc.split('_', 2)
                domain_.append(s[0])
                subdomain_.append(s[1])
                downloaddate_.append(s[2])
                type_.append('rss')
                
            out = pd.DataFrame(
                [date_, title_, descr_, url_, domain_, subdomain_, downloaddate_, type_]).transpose()
            out.columns = columns

            df = pd.concat([df, out])
        
        except:
            pass
        
df = pd.concat([df, out])
df = df.drop_duplicates()
df.to_csv('../data/rss_compiled.csv', encoding='utf-8')
print(df.head())
print(len(df), '= df length')
