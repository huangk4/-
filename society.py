#coding:utf-8
from pymongo import MongoClient
from flask import Flask, request, session, redirect, \
    render_template, url_for, flash,jsonify
from werkzeug import secure_filename
import os
import random
import string
import re


#这里写宏和配置信息
g_server_ip='192.168.65.137'
g_server_port=27017
g_db_name='test'  #库名表名先用自己的
g_tb_name='table_one'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])#允许上传的类型
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
    SECRET_KEY = 'development',
    USERNAME = 'admin',
    PASSWORD = 'adadad'
))

app.config['UPLOAD_FOLDER']='static/tmp'#上传文件目录



@app.route('/test_it')
def web_show(param='name',word='ak'): #这里不知道怎么传参数，能解决的就帮忙解决一下
    show='<center>'
    try:
        results=db.person.find({param:word})
        for result in results:            
            show=show+str(result)
            show=show+'<p>'
    except:
        return show
    show=show+'</center>'
    return show
    

#正则表达式，用来将查询结果的字段和值分开显示
#def show_column():
    





@app.route('/')
def main_redirect():
    return redirect(url_for('login'))
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''登录'''
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show'))

@app.route('/show')
def show():
    #待实现
    return render_template('showdb.html')

@app.route('/add', methods=['POST'])
def add_document():
    #添加，待实现
    return redirect(url_for('show'))


def allowed_file(filename):
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
    
    return render_template('upload.html',columns=columns)

    

#查询函数，param为查询字段，word为查询的值
def search(param,word):
   try:
       results=db.person.find({param:word})
       for result in results:
           print(result)
   except:
       print('没有结果')


#邮箱后缀分析函数,查询数据库返回所有邮箱后缀及所占比的字典
def analysis_email():
    wei=[]
    count={}
    results= db.person.find({},{"email":1,"_id":0})
    for result in results:
        if 'email' in result:
            #print(result['email'])
            m=re.search('@.+?\.com',result['email'])
            if m:
                email=m.group()
                #print(type(m.group()))
                if not email in wei:
                    wei.append(m.group())
                    count[email]=1
                else:
                    count[email]+=1
    counts=0
    emails={}
    for i in count:
        counts+=count[i]
    for i in count:
        emails[i]=str(((count[i]/counts)*100)%101)
    print(emails)
    return emails
        

if __name__=='__main__':
    
    #file_insert('wxsuv.txt')
    #search('name','ak')
    #app.run()
    analysis_email()
    

