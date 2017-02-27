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

#配置信息
ALLOWED_EXTENSIONS = set(allowed_filetype)#允许上传的类型
basedir = os.path.abspath(os.path.dirname(__file__))
#-----------------

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

#接受上传文件并导入数据，删除上传文件
@app.route('/upload',methods=['GET','POST'],strict_slashes=False)
def upload(): 
    if request.method=='POST':
        file_dir=os.path.join(basedir,app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 从表单的file字段获取文件，myfile为该表单的name值
        f=request.files['file']  
        # 判断是否是允许上传的文件类型
        if f and allowed_file(f.filename):  
            fname=secure_filename(f.filename)
            # 获取文件后缀
            ext = fname.rsplit('.',1)[1]  
            #随机生成文件名
            tempname=("".join(random.sample(['z','y','x','w','v',\
                                             'u','t','s'],5)).replace(\
                                                 ' ',''))
            # 修改了上传的文件名
            new_filename=tempname+'.'+ext
            #保存文件到upload目录
            f.save(os.path.join(file_dir,new_filename))  

            #txt以' '分开，csv以','分开
            fenge=' '
            if ext=='txt':
                fenge=' '
            else:
                fenge=','

            #判断文件是否成功保存
            path='static\\tmp\\'+new_filename
            if (not os.path.exists(path)):
                #print('no file')
                return

            #读取文件转换格式插入数据库
            fp=open(path,'r')
            for line in fp:
                linedata={}
                line=line.strip('\n')
                group=line.split(fenge)    
                for key in group:
                    data=key.split(':')
                    linedata[data[0]]=data[1]
                #print(linedata)
                db.person.save(linedata)
            db.person.find()

            #关闭文件，删除文件
            fp.close()
            os.remove(path)
            return "上传成功"
        else:
            return "上传失败"

#单条导入
@app.route('/insert_one',methods=['GET','POST'],strict_slashes=False)
def insert_one():
    if request.method == 'POST':
        for line in db.person.find().limit(1):
            pass
    
        linedata={}
        for i in line:
            if i=='_id':
                continue
            linedata[i]=request.form[i]
        db.person.save(linedata)
        return 'success'

#信息导入页面
@app.route('/insert_data')
def main_upload():

    for line in db.person.find({},{"_id":0}).limit(1):
        #返回一行数据,{"_id":0}即不显示_id
        pass

    #columns为所有列名的列表
    columns=[]
    for i in line:
        columns.append(i)
    
    columns.sort()

    return render_template('upload.html',columns=columns)

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

# #查询函数，param为查询字段，word为查询的值
# def search(param,word):
#    try:
#        results = db.person.find({param:word})
#        for result in results:
#            print(result)
#    except:
#        print('没有结果')

if __name__=='__main__':
    app.run()
    

