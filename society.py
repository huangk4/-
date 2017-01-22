from pymongo import MongoClient

client = MongoClient('192.168.65.137', 27017)
db_name = 'db'
db = client[db_name]
con_action= db['action']
print(db.post)



