import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['Dan']
mycol = mydb['orders']

myquery = { 'size': 'medium' }

mydoc = mycol.find(myquery, {"name":1, "date": 1})

for x in mydoc:
  print(x)
