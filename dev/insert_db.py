#!/usr/bin/python2.7
from pymongo import MongoClient
from pie import get_data
import json

tmp =()
client = MongoClient()

db= client.movie_db
if(db.movie_db.count() > 0):
	db.movie_db.delete_many({})

tmp = get_data(3)

print tmp[0]
for i in tmp:
	# db.movie_db.insert(json.loads(i))
	result = db.movie_db.insert_one(
		json.loads(tmp[0]))
	print result
print db.movie_db.count()
	

	