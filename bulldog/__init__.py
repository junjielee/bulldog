# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_restful import Api
from bulldog.settings import config
from bulldog.views.apis import JobInfo
from bulldog.views.main import main_bp


def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'dev')

    app = Flask('bulldog')
    app.config.from_object(config[config_name])
    Bootstrap(app)

    register_blueprints(app)
    register_apis(app)

    return app


def register_blueprints(app):
    app.register_blueprint(main_bp, url_prefix='/')


def register_apis(app):
    api = Api(app)
    api.add_resource(JobInfo, '/api/jobs')


app = create_app()