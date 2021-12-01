# -*- coding: utf-8 -*-
__author__ = 'NguyenPV'

import os

# app
TESTING = False
DEBUG = True
LOG_FOLDER = 'logs'

# recommendation_systems mysql database
DB_HOST = 'localhost'
DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_PORT = 3306
DB_DATABASE = 'nethubtv_ws_comment'
DB_TABLE_PREFIX = ''



BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# python interpreter
#PYTHON_INTERPRETER = '/usr/bin/python3'
PYTHON_INTERPRETER = 'c:/Python38/python3'

APP_PORT = 5000


