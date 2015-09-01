#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def insert_data(data, db):

    # Your code here. Insert the data into a collection 'arachnid'
    for d in data:
        db.arachnid.insert(d);


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    # Python Mongo use database
    db = client.SPIDERDB

    with open('../arachnid.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print db.arachnid.find_one()