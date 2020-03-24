# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.raffle.util import get_all_raffles
from app.task.util import get_all_tasks

from app.base.models import User
from app.base.util import get_balance_anticaptcha
import json


@blueprint.route('/index')
@login_required
def index():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    user = User.query.filter_by(username=current_user.username).first()

    try:
        logs = json.loads(user.others)
    except:
        logs = {'data': {'logs': []}}

    try:
        config = json.loads(user.config)
        profiles = json.loads(user.profiles)
    except:
        notsetup = True
        return render_template('index.html',
                               notsetup=notsetup,
                               logs=logs,
                               api=get_balance_anticaptcha(config['anticaptcha'])
                               )

    return render_template('index.html',
                           logs=logs,
                           api=get_balance_anticaptcha(config['anticaptcha'])
                           )


@blueprint.route('/raffles')
@login_required
def raffles():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    shoes = get_all_raffles()
    return render_template('raffles.html', shoes=shoes, totalshoes=len(shoes))


@blueprint.route('/documentation')
@login_required
def documentation():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    return render_template('documentation.html')


@blueprint.route('/profiles/<int:id>')
@login_required
def add_profiles(id):

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    return render_template('profiles-page.html')


# @blueprint.route('/<template>')
# @login_required
# def route_template(template):

#     if not current_user.is_authenticated:
#         return redirect(url_for('base_blueprint.login'))

#     try:

#         return render_template(template + '.html')

#     except TemplateNotFound:
#         return render_template('page-404.html'), 404

#     except:
#         return render_template('page-500.html'), 500
