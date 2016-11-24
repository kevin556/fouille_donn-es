from pymongo import MongoClient
# from pie import get_data
import json

def showData():
	print("showData")
	client = MongoClient()
	db = client.data
	print db.data.count()
	cursor = db.data.find()

	for document in cursor:
		print(document)    

def insertData(field,value):
	client = MongoClient()
	db = client.data
	if(db.data.count() > 0):
		db.data.delete_many({})
	print("insertData")
	print(field)
	print(value)
	value = {"author": "Mike",
		"text": "My first blog post!"}
	db.data.insert_one(value)
	print db.data.count(), "datas inserted"
	print("inserData:finish")



	# print("inserData:")
	

	# db.data.insert_one(json.loads(str("{"+field + ":"+ value+ "}")))



