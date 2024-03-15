# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImdbPipeline:
    def process_item(self, item, spider):
        return item


class NoneFilterPipeline:
    def process_item(self, item, spider):
        for key, value in item.items():
            if value is None:
                item[key] = ''
        return item
