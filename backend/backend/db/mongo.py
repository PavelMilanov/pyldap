import pymongo


class MongoConnector:
    
    def __init__(self, user: str, password: str, ip: str = 'localhost', port: int = 27017):
        connect_uri = f'mongodb://{user}:{password}@{ip}:{port}'
        self.client =  pymongo.MongoClient(connect_uri)
        self.db = self.client.store
    
    def create_customer_index(self):
        """Create index for customer['name']"""        
        result = self.db.customers.create_index([('name', pymongo.ASCENDING)], unique=True)
    
    def drop_customers_collection(self):        
        result = self.db.customers.drop()
        return result

    def insert_items(self, data):
        result = self.db.customers.insert_many(data)
        return result.inserted_ids