#coding:utf-8
import sys
import re
import json

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
                return
        if argv[point]=='-f':
            try:
                fname=argv[point+1]
                data_file=open(fname,'r')
                point+=1
            except IOError:
                print('数据文件打开失败')
                return
    columns=[]
    for column in json_file:
        columns.append(json_file[column])


    ext = fname.rsplit('.',1)[1]  
    fenge=' '
    if ext=='txt':
        fenge=' '
    else:
        fenge=','
    for line in data_file:
        if line=='\n':
            continue
        linedata={}
        line=line.strip('\n')
        group=line.split(fenge)
        i=0
        for key in group:
            linedata[columns[i]]=group[i]
            i+=1
        #print(linedata)
        db.person.save(linedata)

    print('导入成功')
    data_file.close()

if __name__=='__main__':
    command_import(sys.argv)
