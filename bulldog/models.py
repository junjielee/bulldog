# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient, DESCENDING
from bulldog.settings import config

config_name = os.getenv('FLASK_CONFIG', 'dev')
db_mongo = MongoClient(config[config_name].MONGO_URI)['positions']['lagou']


def find_jobs(condition):
    return db_mongo.find(condition, {
        "_id": -1,
        "positionName": 1,
        "companyLogo": 1,
        "companyFullName": 1,
        "city": 1,
        "positionId": 1,
    }).sort("_id", DESCENDING)