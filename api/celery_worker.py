#!/usr/bin/env python
from os import environ

from app import celery, create_app
from app.celery_utils import init_celery


from config import config_dict

get_config_mode = environ.get('APPSEED_CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid APPSEED_CONFIG_MODE environment variable entry.')

app = create_app(config_mode)
init_celery(celery, app)
