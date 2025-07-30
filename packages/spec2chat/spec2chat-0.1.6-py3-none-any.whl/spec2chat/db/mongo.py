from pymongo import MongoClient
import os

class MongoDB:
    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(mongo_uri)

    def get_collection(self, db_name, collection_name):
        db = self.client[db_name]
        return db[collection_name]