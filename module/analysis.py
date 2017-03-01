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
        emails[i]=(str(round(((count[i]/counts)*100)%101,1))+'%')
    print(emails)
    return emails

#来源分析函数,查询数据库返回所有来源及所占比的字典
def analysis_source():
    wei=[]
    count={}
    results= db.person.find({},{"source":1,"_id":0})
    for result in results:
        if 'source' in result:
            source=result['source']
            if not source in wei:
                wei.append(source)
                count[source]=1
            else:
                count[source]+=1
    counts=0
    sources={}
    for i in count:
        counts+=count[i]
    for i in count:
        sources[i]=(str(round(((count[i]/counts)*100)%101,1))+'%')
    return sources

#泄露时间分析函数,查询数据库返回所有泄露时间及所占比的字典
def analysis_xtime():
    wei=[]
    count={}
    results= db.person.find({},{"xtime":1,"_id":0})
    for result in results:
        if 'xtime' in result:
            xtime=result['xtime']
            if not xtime in wei:
                wei.append(xtime)
                count[xtime]=1
            else:
                count[xtime]+=1
    counts=0
    xtimes={}
    for i in count:
        counts+=count[i]
    for i in count:
        xtimes[i]=(str(round(((count[i]/counts)*100)%101,1))+'%')
    return xtimes
