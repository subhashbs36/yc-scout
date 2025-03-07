from __future__ import absolute_import

import json
import scrapy
from urllib.parse import urljoin
from ycombinator.items import YCombinatorItem  # Import your item class


def make_start_urls_list():
    """Returns a list with the start URLs."""
    with open('ycombinator/start_urls.txt', 'r') as f:
        return eval(f.read())


class YCombinator(scrapy.Spider):
    """Crawls ycombinator.com/companies and extracts data about each company."""
    name = 'YCombinatorScraper'
    start_urls = make_start_urls_list()

    def parse(self, response):
        # Extract JSON data
        st = response.css('[data-page]::attr(data-page)').get()
        if st is not None:
            # Load the JSON object and set the variable for the 'Company' data
            jo = json.loads(st)['props']
            jc = jo['company']
            
            # Extract image URLs
            image_urls = response.css('img::attr(src)').getall()
            
            # Make URLs absolute if they are relative
            image_urls = [urljoin(response.url, url) for url in image_urls]
            
            # Create an item and yield the data
            item = YCombinatorItem()
            item['company_id'] = jc['id']
            item['company_name'] = jc['name']
            item['short_description'] = jc['one_liner']
            item['long_description'] = jc['long_description']
            item['batch'] = jc['batch_name']
            item['status'] = jc['ycdc_status']
            item['tags'] = jc['tags']
            item['location'] = jc['location']
            item['country'] = jc['country']
            item['year_founded'] = jc['year_founded']
            item['num_founders'] = len(jc['founders'])
            item['founders_names'] = [f['full_name'] for f in jc['founders']]
            item['team_size'] = jc['team_size']
            item['website'] = jc['website']
            item['cb_url'] = jc['cb_url']
            item['linkedin_url'] = jc['linkedin_url']
            item['image_urls'] = image_urls  # Pass image URLs here
            
            yield item