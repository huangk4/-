import sys
sys.path.append("../")
import s_config.py


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
                if line=='\n':
                    continue
                linedata={}
                line=line.strip('\n')
                group=line.split(fenge)    
                for key in group:
                    data=key.split(':')
                    linedata[data[0]]=data[1]
                #print(linedata)
                db.person.save(linedata)

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
