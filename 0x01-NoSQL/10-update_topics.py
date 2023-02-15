#!/usr/bin/env python3
"""This changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """mongo_collection will be the pymongo collection object
    name is a string will be the school name to update
    topics is a list of strings will be the list of topics approached
    in the school"""
    myquery = { "name": name }
    newTopics = { "$set": { "topics": topics } }
    mongo_collection.update_many(myquery, newTopics)
