# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app import celery

import hashlib
import binascii
import os
import io
import random
import string
from flask_login import (
    current_user,
    login_required
)
import csv
import json
import requests
from app import db
from datetime import datetime, timedelta
import jwt
from config import Config

def hash_pass(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


class Settings:
    def __init__(self):
        from app.base.models import User
        # Load Profiles
        user = User.query.filter_by(username=current_user.username).first()

        self.configs = json.loads(user.config)

        # Config
        self.anticaptcha = self.configs['anticaptcha']
        self.delay = self.configs['delay']
        self.proxies = self.configs['proxies']
        self.webhooks = self.configs['webhooks']

    def load_profile_by_id(self, profile_id):
        self.profiles = get_profiles_by_id(profile_id)
        print(self.profiles)
        # Information
        self.address = self.profiles['address']
        self.aptsuite = self.profiles['aptsuite']
        self.cardno = self.profiles['cardno']
        self.city = self.profiles['city']
        self.country = self.profiles['country']
        self.cvv = self.profiles['cvv']
        self.email = self.profiles['email']
        self.expmonth = self.profiles['expmonth']
        self.expyear = self.profiles['expyear']
        self.firstname = self.profiles['firstname']
        self.housenumber = self.profiles['housenumber']
        self.lastname = self.profiles['lastname']
        self.phonenumber = self.profiles['phonenumber']
        self.stateprovince = self.profiles['stateprovince']
        self.zipcode = self.profiles['zipcode']

        # Additional Settings
        self.password = self.randomize()
        if self.email == 'random':
            self.email = self.firstname + self.randomize() + '@gmail.com'
        if self.phonenumber == 'random':
            self.phonenumber = self.phn()

    def random(self):
        self.email = self.firstname + self.randomize() + '@gmail.com'
        self.phonenumber = self.phn()
        self.password = self.randomize()

    def phn(self):
        p = list('0000000000')
        p[0] = str(random.randint(1, 9))
        for i in [1, 2, 6, 7, 8]:
            p[i] = str(random.randint(0, 9))
        for i in [3, 4]:
            p[i] = str(random.randint(0, 8))
        if p[3] == p[4] == 0:
            p[5] = str(random.randint(1, 8))
        else:
            p[5] = str(random.randint(0, 8))
        n = range(10)
        if p[6] == p[7] == p[8]:
            n = (i for i in n if i != p[6])
        p[9] = str(random.choice(n))
        p = ''.join(p)
        return p[:3] + p[3:6] + p[6:]

    def randomize(self, size=13, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


def send_log(type, message):
    now = datetime.now()
    current_time = now. strftime("%H:%M:%S")
    # Open Query
    from app.base.models import User
    user = User.query.filter_by(username=current_user.username).first()
    try:
        data = json.loads(user.others)
    except:
        data = {'data': {
            'logs': []
        }}

    data['data']['logs'].append({
        "type": type,
        "message": message,
        "time": current_time
    })
    datajson = json.dumps(data)
    setattr(user, 'others', datajson)
    db.session.commit()
    print('log sent')
    return {'msg': 'success'}


def clear_logs():
    from app.base.models import User
    user = User.query.filter_by(username=current_user.username).first()

    data = {'data': {
            'logs': []
            }}
    datajson = json.dumps(data)
    setattr(user, 'others', datajson)
    db.session.commit()
    return {'msg': 'success'}


def read_csv(data_db, file_byte):
    id = len(data_db['data']) + 1
    csv_reader = csv.DictReader(io.StringIO(file_byte))
    datas = []
    for row in csv_reader:
        row['id'] = id
        datas.append(row)
        id += 1

    return datas


def get_profiles_by_id(profileid):
    from app.base.models import User
    user = User.query.filter_by(username=current_user.username).first()
    datas = json.loads(user.profiles)
    for data in datas['data']:
        if str(data['id']) == str(profileid):
            return data

    return False

def get_balance_anticaptcha(apikey):
    r = requests.get('https://api.anti-captcha.com/getBalance', json={'clientKey':apikey})
    
    return r.json()

def encrypt_jwt(username):
    return jwt.encode({'username':username,'exp': datetime.utcnow() + timedelta(seconds=1)},Config.SECRET_KEY)

def decrypt_jwt(token):
    try:
        decode = jwt.decode(token, Config.SECRET_KEY, leeway=10, algorithms=['HS256'])
        return decode
    except:
        # Return false if expired
        return False

