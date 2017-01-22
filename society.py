from pymongo import MongoClient



#这里写宏
g_server_ip='192.168.65.137'
g_server_port=27017
g_db_name='test'  #库名表名先用自己的
g_tb_name='table_one'

##########


client = MongoClient(server_ip,server_port)
db = client[g_db_name]
print(db.post)



