#!/usr/bin/env python3
"""This returns a list of schools having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """mongo_collection will be the pymongo collection object
    topic(string) will be the topic searched"""
    return [doc for doc in mongo_collection.find({ "topics": topic })]
