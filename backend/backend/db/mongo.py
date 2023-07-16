from pymongo import MongoClient


class MongoConnector:
    
    def __init__(self, user: str, password: str, ip: str = 'localhost', port: int = 27017):
        connect_uri = f'mongodb://{user}:{password}@{ip}:{port}'
        self.client =  MongoClient(connect_uri)
        self.db = self.client.store
        self.collection = self.db.customers
    
    def insert_items(self, data):
        result = self.collection.insert_many(data)
        print(result)