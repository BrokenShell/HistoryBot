import datetime
import os

import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv


class Collection:
    load_dotenv()
    client = MongoClient(os.getenv('MONGO_URL'))
    projection = {"_id": False, "timestamp": False}

    def __init__(self, database: str, collection: str):
        self.col = self.client[database][collection]
        self.col.create_index([("$**", "text")])

    def write(self, record: dict) -> bool:
        return self.col.insert_one(self.timestamp(record)).acknowledged

    def write_many(self, records: list[dict]):
        return self.col.insert_many(map(self.timestamp, records))

    def recent(self, count: int):
        return self.col.find({}, self.projection).sort("timestamp").limit(count)

    def search(self, query: str, count: int) -> list[dict]:
        query = {"$text": {"search": query}}
        return list(self.col.find(query, self.projection).limit(count))

    def timestamp(self, record: dict) -> dict:
        record.update({"timestamp": datetime.datetime.now()})
        return record
