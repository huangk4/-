#coding:utf-8
import sys
import re
import json
from itertools import islice
from pymongo import MongoClient

g_server_ip='192.168.65.137'	#mongodb数据库地址
g_server_port=27017		#数据库端口
g_db_name='test'  		#数据库名
g_tb_name='table_one'		#数据表名
#获取mongodb客户端
client = MongoClient(g_server_ip,g_server_port)
#获取所要操作的数据库
db = client[g_db_name]

def command_import(argv):
    point=0
    while not point ==4:
        point+=1
        if argv[point]=='-format':
            try:
                with open(argv[point+1],'r') as f:
                    json_file=json.load(f)
                point+=1
            except IOError:
                print('格式文件打开失败')
                return '格式文件打开失败'
        if argv[point]=='-f':
            try:
                fname=argv[point+1]
                data_file=open(fname,'r')
                point+=1
            except IOError:
                print('数据文件打开失败')
                return '数据文件打开失败'
    columns=[]
    for column in json_file:
        columns.append(json_file[column])


    #从id_0确定分隔符
    fenge=columns[0]
    column=data_file.readline().strip('\n').split(fenge)
    num=[]
    t=0
    for i in column:
        if i in columns:
            num.append(t)
            
        t+=1

    for line in islice(data_file,0,None):
        if line=='\n':
            continue
        linedata={}
        line=line.strip('\n')
        group=line.split(fenge)
        
        for i in num:
            linedata[column[i]]=group[i]
        #print(linedata)
        db.person.save(linedata)

    print('导入成功')
    data_file.close()
    return '导入成功' 

if __name__=='__main__':
    command_import(sys.argv)
