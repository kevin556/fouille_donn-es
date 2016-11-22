from pymongo import MongoClient
from pie import get_data
import json

def showMovies():
	client = MongoClient()
	db = client.movie_db
	cursor = db.movie_db.find()
	
	for document in cursor:
	    print(document['Title'])    

# showMovies()



# Retourne un tableau contenant des films
def getFilmsByTitle(name):
	client = MongoClient()
	db = client.movie_db
	cursor = db.movie_db.find({"Title": name})
	res = []
	for document in cursor:
		res.append(document)
		print("title =" , document['Title'], "actors = ",document['Actors'])
	return res

getFilmsByTitle("Eye Contact 31")