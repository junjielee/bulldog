# -*- coding: utf-8 -*-

from flask import render_template, Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def hello():
    return render_template('index.html')
