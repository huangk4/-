#coding:utf-8
from pymongo import MongoClient
from flask import Flask


#这里写宏
g_server_ip='192.168.65.137'
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

@app.route('/')
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
    





if __name__=='__main__':
    app.run()
    


#查询函数，param为查询字段，word为查询的值
def search(param,word):
    try:
        results=db.person.find({param:word})
        for result in results:
            print(result)
    except:
        print('没有结果')

'''
#删除表
db.person.drop() 

#网数据库集合中添加数据
db.person.save({'name':'ak2','email':'5542323478@qq.com',\
                'password':'admin','passwordHash':'E45345HGFGRRRDFFGHSDHF3Y98HFG49H'})

#查询数据库集合中所有数据
results=db.person.find()
for result in results:
    print(result)
print(db.post)
'''


