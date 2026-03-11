#!/usr/bin/env python

# add imports here
from pymongo import MongoClient, errors
import os

# add variables
url = os.environ.get('MONGODB_ATLAS_URL')
user = os.environ.get('MONGODB_ATLAS_USER') 
pwd = os.environ.get('MONGODB_ATLAS_PWD')

def main():
    client = MongoClient(url,username=user,password=pwd,connectTimeoutMS=200,retryWrites=True)
    db = client.bookstore
    authors = db.authors
    docs = authors.count_documents({})
    print("Total number of author documents:", docs)
    for author in authors.find():
        name = author.get("name")
        nationality = author.get("nationality")
        print("Name: ", name, "| Nationality: ", nationality)
    
    client.close() 

if __name__ == "__main__":
    main()
