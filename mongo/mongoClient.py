from pymongo import MongoClient


class DataBase:
    def __init__(self, db_name: str) -> None:
        self.client = MongoClient(
            "mongodb+srv://narek:narek@cluster0.debap.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client[db_name]

    def is_connected(self):
        return self.client['connect']

    def get_collection(self, collection_name: str):
        return self.db[collection_name]
