### Adelph Policy Iniative
##### Backscraping Middle East News

<br>**Files**<br>
*Scripts*

rss_scraper.py
- Downloads all rss sites of interest

scrapy_{news site name}.py
- Backscraper {news site name} using the Scrapy package to iterate archives
- One per site domain due to unique page structure

*Tables*
source_feeds.csv
- List containing websites and subdomains to scrape.
- Contains rss url and descritption of type of backscraping code needed
