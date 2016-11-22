#!/usr/bin/python2.7
from pymongo import MongoClient
from pie import get_data
import json
	
def insert(data):

	client = MongoClient()
	# purge la table movies
	db = client.movie_db
	# if(db.movie_db.count() > 0):
	# 	db.movie_db.delete_many({})
	for i in range(0,len(data),1):
		tmp = json.loads(data[i])
		result = db.movie_db.insert_one(tmp)
		print(tmp['Title'])

	print db.movie_db.count(), "movies inserted"


def clearDataBase():
	client = MongoClient()
	# purge la table movies
	db = client.movie_db
	if(db.movie_db.count() > 0):
		db.movie_db.delete_many({})



	
# Hydrate la base de donnees
# nb : nombre de films qu'on souhaite inserer
def hydrate_movies(nb):
	clearDataBase()
	try:
		movies = get_data(nb)
		insert(movies)
	except Exception:
	    pass
	

hydrate_movies(10)