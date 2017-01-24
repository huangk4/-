#coding:utf-8
from pymongo import MongoClient
from flask import Flask, request, session, redirect, \
    render_template, url_for, flash


#这里写宏
g_server_ip='127.0.0.1'
g_server_port=27017
g_db_name='test'  #库名表名先用自己的
g_tb_name='table_one'
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

if __name__=='__main__':
    app.run()
    


# @app.route('/')
# def web_show(param,word): #这里不知道怎么传参数，能解决的就帮忙解决一下
#     show='<center>'
#     try:
#         results=db.person.find({param:word})
#         for result in results:            
#             show=show+str(result)
#             show=show+'<p>'
#     except:
#         return show
#     show=show+'</center>'
#     return show
# # #查询函数，param为查询字段，word为查询的值
# def search(param,word):
#     try:
#         results=db.person.find({param:word})
#         for result in results:
#             print(result)
#     except:
#         print('没有结果')

# #正则表达式，用来将查询结果的字段和值分开显示
# def show_column():