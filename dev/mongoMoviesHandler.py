#!/usr/bin/python2.7

from pymongo import MongoClient
from pie import get_data
import json

def showMovies():
	client = MongoClient()
	db = client.movie_db
	print db.movie_db.count()
	cursor = db.movie_db.find()

	for document in cursor:
	    print(document['Title'])    
	    # print document

# showMovies()
try:
	showMovies()
except KeyError:
	print "Le film n'a pas de titre"
	pass


def getFilmsByTitle(name):
	client = MongoClient()
	db = client.movie_db
	cursor = db.movie_db.find({"Title": name})
	res = []
	for document in cursor:
		res.append(document)
		print("title =" , document['Title'], "actors = ",document['Actors'])
	return res


def getFilmsByGenre(genre):
	client = MongoClient()
	db = client.movie_db
	cursor = db.movie_db.find({"Genre": genre})
	res = []
	for document in cursor:
		res.append(document)
		print("title =" , document['Title'], "actors = ",document['Actors'])
	return res

def getFilmsByYear(year):
	client = MongoClient()
	db = client.movie_db
	cursor = db.movie_db.find({"Year": year})
	res = []
	for document in cursor:
		res.append(document)
		print("title =" , document['Title'], "actors = ",document['Actors'])
	return res

def getFilmsByCountry(country):
	client = MongoClient()
	db = client.movie_db
	cursor = db.movie_db.find({"Country": country})
	res = []
	for document in cursor:
		res.append(document)
		print("title =" , document['Title'], "actors = ",document['Actors'])
	return res

# Recuperer uniquement les films (pas les series ...)
def getFilms():
	client = MongoClient()
	db = client.movie_db
	cursor = db.movie_db.find({"Type": "movie"})
	res = []
	for document in cursor:
		res.append(document)
		print("title =" , document['Title'], "actors = ",document['Actors'])
	return res

# getFilmsByYear("2005")
# getFilmsByTitle("Eye Contact 31")
# def getFilmsByActors(actors):





