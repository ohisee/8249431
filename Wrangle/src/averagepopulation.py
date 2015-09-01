#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use an aggregation query to answer the following question. 

Extrapolating from an earlier exercise in this lesson, find the average regional city population 
for all countries in the cities collection. What we are asking here is that you first calculate the 
average city population for each region in a country and then calculate the average of all the 
regional averages for a country. As a hint, _id fields in group stages need not be single values. 
They can also be compound keys (documents composed of multiple fields). You will use the same 
aggregation operator in more than one stage in writing this aggregation query. I encourage you to 
write it one stage at a time and test after writing each stage.

Please modify only the 'make_pipeline' function so that it creates and returns an aggregation 
pipeline that can be passed to the MongoDB aggregate function. As in our examples in this lesson, 
the aggregation pipeline should be a list of one or more dictionary objects. 
Please review the lesson examples if you are unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. If you want to run this code 
locally on your machine, you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.

Please note that the dataset you are using here is a smaller version of the cities collection used in 
examples in this lesson. If you attempt some of the same queries that we looked at in the lesson 
examples, your results may be different.
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
    pipeline = [{"$match" : {"country" : {"$ne" : None, "$exists" : True}}},
                {"$unwind" : "$isPartOf"},
                {"$group" : {"_id" : {"countryKey": "$country", "regionKey" : "$isPartOf"}, "avgCitiesPup" : {"$avg" : "$population"}}},
                {"$group" : {"_id" : "$_id.countryKey", "avgRegionalPopulation" : {"$avg" : "$avgCitiesPup"}}}];
    return pipeline

def aggregate(db, pipeline):
    result = db.cities.aggregate(pipeline)
    return result

if __name__ == '__main__':
    db = get_db('examples')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    if len(result["result"]) < 150:
        pprint.pprint(result["result"])
    else:
        pprint.pprint(result["result"][:100])
    for country in result["result"]:
        if country["_id"] == 'Algeria':
            assert country["_id"] == 'Algeria'
            assert country["avgRegionalPopulation"] == 187590.19047619047
    assert {'_id': 'Algeria', 
             'avgRegionalPopulation': 187590.19047619047} in result["result"]
