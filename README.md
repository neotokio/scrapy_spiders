# Scrapy Spiders Examples

Respository with Scrapy made web crawlers.

<b>What's inside?</b>

Scrapers use different approach.

*Scraping HTML rendered content using absolute paths
*Scraping HTML rendered content using relative paths (xpath logic selection)
*Scraping JavaScript rendered content using Scrapy-Splash
*Scraping content from local file
*Additional scripts for processing data (Extracting URLS from local HTML File, processing URLS from JSON API)
*JSON pipelines

<b>Usability</b>

All code was written for private use, therefore it's most likley unusable for you. Ie. sometimes we first downloaded all URLs to local file using JSON API, because it was easier than crearting sendForm request in Javascript for parsing each page, however, all files 'needed for work' are in each respository. You will need to make certain tweaks for them to work.

Therefore, you should use this respository mostly as reference when stuck on writing your scrapy logic/xpath logic or when you simply look for some alternative approach.

<b>On what websites those web crawlers work</b>

1. https://alternativedata.org
  *Uses JSON API URLS (local)
  *Advanced xpath selection
2. https://www.go4worldbusiness.com/
  *Simple HTML web crawler
  *Navigates to different pages
3. https://www.indiehackers.com/
  *Uses already preprocessed URLS from downloaded HTML sources (scrape from url_list.txt)
  *Uses scrapy-splash with appropriate settings (IH is suuuuper slow)
4. https://www.tradekey.com/
  *HTML rendered content
  *Advanced multipage navigation
  *href.py files is used for processing tradekeys URLs localy
