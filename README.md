# 寒假项目
##主要功能
###人员信息的导入
- 支持txt、csv等文本格式
- 批量导入
- 自定义字段导入

###人员信息的查询
- 按username查询
- 按email查询
- 按password查询
- 按passwordHash查询
- 按自定义字段组合查询

###人员信息的分析
- 来源分析
- 邮箱后缀
- 泄露时间等

###实现REST API(导入模块除外)

##开发要求
- 数据库采用mongoDB
- 采用python3开发，使用Flask框架

##参考资料
###mongodb
- mongodb数据库操作 http://hackpro.iteye.com/blog/1278105
- python3操作mongodb实例 http://www.2cto.com/kf/201701/584915.html

###Flask
- http://www.jb51.net/article/64434.htm
- http://www.oschina.net/translate/the-flask-mega-tutorial-part-i-hello-world
