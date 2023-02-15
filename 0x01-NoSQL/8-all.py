#!/usr/bin/env python3
"""This lists all documents in a collection"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """Returns a list of all documents in the colection"""
    doc_list = []
    for doc in mongo_collection.find():
        doc_list.append(doc)
    return doc_list
