**Files**<br>
*Scripts*

compilation/main.sh

- runs all spiders
- parses all downloaded rss feeds
- compiles into workable database called: compilation/compile.csv
	- Note: Last cleaning script is under progress and will be added

rss_scraper.py

- Downloads all rss sites of interest
- Set to download everyday via crontab on local machine

spiders/run_spiders.sh

- Runs all spiders and saves with unique name per date
	- Leverages xargs for parallel processing
	- Set to download everyday via crontab on local machine

scrapy/scrapy_{news site name}.py

- Backscraper {news site name} using the Scrapy package to iterate archives
- One per site domain due to unique page structure
- To run, [download scrapy](https://pypi.python.org/pypi/Scrapy), see Scrapy_Overview.ipynb for scrapy primer, then in a terminal type:<br>
```python
scrapy runspider scrapy_{news site name}.py
```

compilation/rss_parse.py

- Parses and compiles all rss feeds

<br>*Tables*<br>

source_feeds.csv
- List containing websites and subdomains to scrape.
- Contains rss url and descritption of type of backscraping code needed
