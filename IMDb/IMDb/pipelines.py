# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem
from dotenv import load_dotenv
import os

load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')

class ImdbPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(ATLAS_KEY)
        self.db = self.client["imdb"]
        self.collection = self.db["top_imdb"]

    def process_item(self, item, spider):
        # Vérifier chaque champ et attribuer une valeur par défaut s'il est manquant
        item = {key: value if value else "" for key, value in item.items()}
        self.collection.insert_one(dict(item))
        return item