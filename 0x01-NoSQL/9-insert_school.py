#!/usr/bin/env python3
"""This inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """This returns the new _id,
    mongo_collection will be the new pymongo collection object"""
    new_result = mongo_collection.insert_one( kwargs )
    return new_result.inserted_id
