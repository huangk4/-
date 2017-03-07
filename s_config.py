'''from pymongo import MongoClient
from flask import Flask, request, session, redirect, \
    render_template, url_for, flash, jsonify, abort
'''

#这里写宏和配置信息
g_server_ip='192.168.65.137'
g_server_port=27017
g_db_name='test'  #库名表名先用自己的
g_tb_name='table_one'
ALLOWED_EXTENSIONS = ['txt', 'csv']
#-----------------

#默认配置
#flask app config
app = Flask(__name__)

debug = True,
secret_key = 'development',
usr_name = 'admin',
usr_pwd = 'adadadad',
upload_dir = 'static/tmp'

app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = secret_key,
    USERNAME = usr_name,
    PASSWORD = usr_pwd,
    UPLOAD_FOLDER = upload_dir
))
