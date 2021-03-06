from flask import Flask, request, json, Response
from pymongo import MongoClient
from data.config import *

class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.mo20d.mongodb.net/Song?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)  
      
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def read_one(self, song_id):
        documents = self.collection.find_one({"song_id":{"$eq": song_id}}, {"_id": 0})
        output = documents
        return output

    def write(self, data):
        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

if __name__ == '__main__':
    data = {
        "database": f"{database_name}",
        "collection": f"{collection_name}",
    }
    mongo_obj = MongoAPI(data)
    print(json.dumps(mongo_obj.read(), indent=4))