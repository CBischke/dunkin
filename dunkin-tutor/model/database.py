from commons import properties
from pymongo import MongoClient
from bson import ObjectId

class Database:
    def __init__(self, url=properties.DB_URL, 
                        port=properties.DB_PORT, 
                        db_name=properties.DB_NAME, 
                        collection=properties.DB_COLLECTION):
        self.client = MongoClient(url,port)
        self.db = self.client[db_name]
        self.collection = self.db[collection]

    def close(self):
        self.client.close()

    def save_to_db(self, json_to_save):
        self.collection.insert_one(json_to_save)

    def delete_collection(self):
        self.collection.drop()