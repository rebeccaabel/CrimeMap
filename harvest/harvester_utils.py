from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

def get_db_connection(mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    db = client[db_name]
    return db, client, db[collection_name]

def upsert_article(collection, article_data):
    result = collection.update_one(
        {
            "title": article_data["title"],
            "date": article_data["date"],
            "link": article_data["link"]
        },
        {
            "$set": article_data
        },
        upsert=True
    )
    return result
