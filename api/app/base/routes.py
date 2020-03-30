# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User

from app.base.util import send_log, clear_logs, verify_pass, read_csv, get_profiles_by_id, encrypt_jwt, decrypt_jwt

import requests
import json
import os



@blueprint.route('/')
def route_default():
    # shoe = Shoes(name='Raihan')
    # db.session.add(shoe)
    # db.session.commit()
    return jsonify({'msg':encrypt_jwt('lmao').decode('utf8')})


@blueprint.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

## Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            # # Check License
            # validation = requests.post('https://xserver.boxmarshall.com/api/v2/authorize/validate/no-device',
            #                            json={"serialkey": current_user.licensekey})
            # if validation.status_code == 200:
            #     login_user(user)
            #     session.permanent = True
            #     return redirect(url_for('base_blueprint.route_default'))
            # else:
            #     return render_template('login/login.html', msg='License invalid or expired', form=login_form)
            login_user(user)
            session.permanent = True
            return redirect(url_for('base_blueprint.route_default'))
        # Something (user or pass) is not ok
        return render_template('login/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template('login/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    licensekey = request.json['licensekey']

    # Check License
    validation = requests.post('https://xserver.boxmarshall.com/api/v2/authorize/validate/no-device',
                                json={"serialkey": licensekey})

    if validation.status_code == 200:

        user = User.query.filter_by(username=username).first()
        print(user)
        if user:
            return jsonify({'status':'invalid username','msg':'Username is already taken'}),400

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'status':'invalid email','msg':'Email already registered'}),400

        user = User.query.filter_by(licensekey=licensekey).first()
        if user:
            return jsonify({'status':'invalid key','msg':'Key is already used'}),400
        # else we can create the user
        user = User(**request.json)
        db.session.add(user)
        db.session.commit()

        return jsonify({'status':'success','token':encrypt_jwt(user.username).decode('utf8')})

    else:
        return jsonify({'status':'invalid key','msg':'Key doesn\'t exists or expired'}),400


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'GET':
        user = User.query.filter_by(username=current_user.username).first()

        try:
            data = json.loads(user.config)
        except:
            data = {
                'apikey': '',
                'webhook': '',
                'delay': '',
                'proxies': ''
            }
        return render_template('settings.html')

    if request.method == 'POST':
        apikey = request.form['anticaptcha']
        webhooks = request.form['webhooks']
        delay = request.form['delay']
        proxies = request.form['proxies']
        dataraw = {
            'apikey': apikey,
            'webhook': webhooks,
            'delay': delay,
            'proxies': proxies
        }

        datajson = json.dumps(dataraw)
        user = User.query.filter_by(username=current_user.username).first()
        setattr(user, 'config', datajson)
        db.session.commit()
        return render_template('settings.html')


@blueprint.route('/profiles', methods=['GET', 'POST'])
@login_required
def profiles():
    if request.method == 'GET':
        return render_template('profiles.html')

    if request.method == 'POST':
        return render_template('profiles.html')


@blueprint.route('/v1/profiles', methods=['GET', 'POST', 'DELETE'])
@login_required
def settings_profiles():
    if request.method == 'GET':
        user = User.query.filter_by(username=current_user.username).first()

        # Get data from db
        try:
            data = json.loads(user.profiles)
        except:
            data = {'data': []}

        return data
    if request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()

        try:
            data = json.loads(user.profiles)
        except:
            data = {'data': []}
        newdata = {}

        newdata['id'] = len(data['data']) + 1
        for i in request.form:
            newdata[i] = request.form[i]

        data['data'].append(newdata)
        datajson = json.dumps(data)
        setattr(user, 'profiles', datajson)
        db.session.commit()
        return {'msg': 'profile updated'}
    if request.method == 'DELETE':
        user = User.query.filter_by(username=current_user.username).first()
        id = request.json['id']

        try:
            datas = json.loads(user.profiles)
        except:
            return {'msg': 'no profiles found!'}, 400

        temp_dict = {"data": []}
        for data in datas['data']:
            if str(data['id']) != str(id):
                temp_dict['data'].append(data)
        datajson = json.dumps(temp_dict)
        setattr(user, 'profiles', datajson)
        db.session.commit()
        return {'msg': 'deleted!'}


@blueprint.route('/v1/profiles/<int:id>')
@login_required
def getprofilesid(id):
    return {'data': get_profiles_by_id(id)}


@blueprint.route('/v1/config', methods=['GET', 'POST'])
@login_required
def settings_config():
    if request.method == 'GET':
        user = User.query.filter_by(username=current_user.username).first()

        try:
            data = json.loads(user.config)
        except:
            data = {
                'username': current_user.username
            }
        return {'data': data}
    if request.method == 'POST':
        print(request.data)
        dataraw = {}

        for i in request.form:
            dataraw[i] = request.form[i]

        datajson = json.dumps(dataraw)
        user = User.query.filter_by(username=current_user.username).first()
        setattr(user, 'config', datajson)
        db.session.commit()
        return {'msg': 'config updated'}


@blueprint.route('/v1/import', methods=['POST'])
@login_required
def settings_import():
    if request.method == 'POST':
        file_val = request.files['file']
        if file_val.filename.split('.')[-1] == 'csv':
            file_str = file_val.read().replace(b'\r', b'').decode("utf-8")

            user = User.query.filter_by(username=current_user.username).first()
            try:
                data_db = json.loads(user.profiles)
            except:
                data_db = {'data': []}

            for i in read_csv(data_db, file_str):
                data_db['data'].append(i)
            data = json.dumps(data_db)

            print(data)
            setattr(user, 'profiles', data)
            db.session.commit()
            return {'msg': 'success'}, 200
        else:
            print('invalid format')
            return {'msg': 'failed'}, 400


@blueprint.route('/v1/others', methods=['GET'])
@login_required
def settings_others():
    if request.method == 'GET':
        user = User.query.filter_by(username=current_user.username).first()

        try:
            data = json.loads(user.others)
        except:
            data = {
                'logs': []
            }
        return data
    if request.method == 'POST':
        send_log(request.json['type'], request.json['message'], request.json['time'])
        return {'msg': 'log sent'}


@blueprint.route('/v1/clear_logs')
@login_required
def clear_log():
    clear_logs()
    return {'msg': 'success'}


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
