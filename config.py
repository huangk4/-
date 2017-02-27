#这里写宏和配置信息
g_server_ip = '127.0.0.1'
g_server_port = 27017
g_db_name = 'test'  #库名表名先用自己的
allowed_filetype = ['txt', 'csv']
#-----------------

#flask的相关配置
secret_key = 'development'
usr_name = 'admin'
usr_pwd = 'adadadad'
upload_dir = 'static/tmp'
APP_URL = 'http://127.0.0.1:5000'
#-----------------

#flask app config
DEBUG = True,
SECRET_KEY = 'development',
USERNAME = 'admin',
PASSWORD = 'adadadad',
UPLOAD_FOLDER = 'static/tmp'