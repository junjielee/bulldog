# -*- coding: utf-8 -*-

import os


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev bulldog')


class DevConfig(BaseConfig):
    DEBUG = True
    MONGO_URI = "mongodb://localhost:27017/positions"


class ProductConfig(BaseConfig):
    DEBUG = False


config = {
    "dev": DevConfig,
    "pro": ProductConfig,
}