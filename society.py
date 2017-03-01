#coding:utf-8
from pymongo import MongoClient
from flask import Flask, request, session, redirect, \
    render_template, url_for, flash, jsonify, abort
from werkzeug import secure_filename
from flask_restful import Api, Resource
import os
import random
import string
import re


#这里导入自定义模块
import s_config
import module.remote_import
import module.base_import
import module.analysis


basedir = os.path.abspath(os.path.dirname(__file__))

#获取mongodb客户端
client = MongoClient(g_server_ip,g_server_port)
#获取所要操作的数据库
db = client[g_db_name]
#-----------------

app = Flask(__name__)

#默认配置
app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = secret_key,
    USERNAME = usr_name,
    PASSWORD = usr_pwd,
    UPLOAD_FOLDER = upload_dir
))
# app.config.from_object('config.py')
# app.config['UPLOAD_FOLDER']='static/tmp'#上传文件目录

class Person(Resource):
    '''人员类'''
    def get(self, name=None, email=None):
        #data用于存储获取到的信息
        data = []

        if name and email:
            persons_info = db.person.find({"name": name, "email": email}, {"_id": 0})
        
        elif name:
            persons_info = db.person.find({"name": name}, {"_id": 0})
        
        elif email:
            persons_info = db.person.find({"email": email}, {"_id": 0})
            
        else:
            persons_info = db.person.find({}, {"_id": 0, "update_time": 0}).limit(10)
            for person in persons_info:
                data.append(person)

            return jsonify({"response": data})
 
        if persons_info:
            for person in persons_info:
                data.append(person)

            return jsonify({"status": "ok", "data": data})
        else:
            return {"response": "no person found for {} {}".format(name, email)}

    def post(self):
        '''
        以json格式进行提交文档
        '''
        data = request.get_json()
        if not data:
            return {"response": "ERROR DATA"}
        else:
            name = data.get('name')
            email = email.get('email')

            if name and email:
                if db.person.find_one({"name": name, "email": email}, {"_id": 0}):
                    return {"response": "{{} {} already exists.".format(name, email)}
                else:
                    db.person.insert(data)
            else:
                return redirect(url_for("person"))
    
    def put(self, name, email):
        '''
        根据name和email进行定位更新数据
        '''
        data = request.get_json()
        db.person.update({'name': name, 'email': email},{'$set': data})
        return redirect(url_for("person"))

    def delete(self, email):
        '''
        email作为唯一值, 对其进行删除
        '''
        db.person.remove({'email': email})
        return redirect(url_for("person"))

#添加api资源
api = Api(app)
api.add_resource(Person, "/api", endpoint="person")
api.add_resource(Person, "/api/name/<string:name>", endpoint="name")
api.add_resource(Person, "/api/email/<string:email>", endpoint="email")

@app.route('/')
def main_redirect():
    '''初始页面定向'''
    # if session['logged_in'] is True:
    #     return redirect(url_for('searchinfo'))
    return redirect(url_for('login'))
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''登录模块'''
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('searchinfo'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    '''登出模块'''
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('searchinfo'))

def allowed_file(filename):
    '''允许上传的文件类型'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS





#查询信息
@app.route('/searchinfo', methods = ['POST', 'GET'])
def searchinfo():
    if request.method == 'POST':
        
        line = []
        for line in db.person.find().limit(1):
            #返回一行数据
            pass

        #columns为所有列名的列表
        columns=[]
        for i in line:
            columns.append(i)        
        columns.sort()

        if request.form.get('type') in ['name', 'email', 'password', 'passwordHash']:
            found = db.person.find({request.form.get('type'):request.form.get('inputinfo')})
            if found:
                flash('successed')
            else:
                flash('failed')
            
            infos = []
            for doc in found:
                infos.append(doc)
                
            return render_template('searchinfo.html', infos=infos, columns=columns)

        else:
            flash('Erorr')
            return render_template('searchinfo.html')
            
    if request.method == 'GET':
        return render_template('searchinfo.html')







    
if __name__=='__main__':


    #file_insert('wxsuv.txt')
    #search('name','ak')
    #app.run()
    #print(analysis_source())
    

    

