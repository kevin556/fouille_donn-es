from pymongo import MongoClient
from pie import get_data
import json

def getFilms():
	client = MongoClient()
	db = client.movie_db
	movies = db.movie_db

	nbMovies = movies.count()
	for i in range(0,nbMovies,1):
		print movies[i]

	return db	




getFilms()