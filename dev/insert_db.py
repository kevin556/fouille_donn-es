#!/usr/bin/python2.7
from pymongo import MongoClient
from pie import get_data
import json

tmp =()
client = MongoClient()

db= client.movie_db
#if(db.movie_db.count() > 0):
#	db.movie_db.delete_many({})

while(True):
	tmp = get_data(1)
	for i in tmp:
		db.movie_db.insert(json.loads(i))

print db.movie_db.count()
db.close()

	