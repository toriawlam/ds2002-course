"""Shared MongoDB connection for mypractice db (used by 02-mongo_setup.py)."""
from pymongo import MongoClient, errors
from bson.json_util import dumps
import pprint
import os

# Use environment variables from README: MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD
uri = os.getenv('MONGODB_ATLAS_URL')
username = os.getenv('MONGODB_ATLAS_USER')
password = os.getenv('MONGODB_ATLAS_PWD')

client = MongoClient(uri, username=username, password=password, connectTimeoutMS=200, retryWrites=True)
db = client.mypractice
items = db.items

if __name__ == "__main__":
    # Fetch list of collections and print total number of docs in each
    for name in db.list_collection_names():
        count = db[name].count_documents({})
        print(f"{name}: {count} documents")
