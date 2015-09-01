#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use an aggregation query to answer the following question. 

Which Region in India has the largest number of cities with longitude between 75 and 80?

Please modify only the 'make_pipeline' function so that it creates and returns an aggregation 
pipeline that can be passed to the MongoDB aggregate function. As in our examples in this lesson, 
the aggregation pipeline should be a list of one or more dictionary objects. 
Please review the lesson examples if you are unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. If you want to run this 
code locally on your machine, you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.

Please note that the dataset you are using here is a smaller version of the twitter dataset used in 
examples in this lesson. If you attempt some of the same queries that we looked at in the lesson 
examples, your results will be different.
"""

"""
{
    "_id" : ObjectId("52fe1d364b5ab856eea75ebc"),
    "elevation" : 1855,
    "name" : "Kud",
    "country" : "India",
    "lon" : 75.28,
    "lat" : 33.08,
    "isPartOf" : [
        "Jammu and Kashmir",
        "Udhampur district"
    ],
    "timeZone" : [
        "Indian Standard Time"
    ],
    "population" : 1140
}
"""

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$match" : {"country" : "India", "name" : {"$ne" : None, "$exists" : True}, "lon" : {"$gte" : 75, "$lte" : 80}}}, 
                {"$unwind" : "$isPartOf"},
                {"$group" : {"_id" : "$isPartOf", "count" : {"$sum" : 1}}},
                {"$sort" : {"count" : -1}},
                {"$limit" : 1}];
    return pipeline

def aggregate(db, pipeline):
    result = db.cities.aggregate(pipeline)
    return result

if __name__ == '__main__':
    db = get_db('examples')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    pprint.pprint(result["result"][0])
    assert len(result["result"]) == 1
    assert result["result"][0]["_id"] == 'Tamil Nadu'

