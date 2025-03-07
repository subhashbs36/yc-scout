# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class CompaniesPipeline:
    def process_item(self, item, spider):
        return item
