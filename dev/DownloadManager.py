#!/usr/bin/python2.7
from random import * 
import urllib2
from pymongo import MongoClient
import json


# Telecharge les films depuis la base de donnees distante
def downloadMovies(number):
	tmp=[]
	max = 1000000
	min = 10000
	a = 0
	tmp_film = ""
	for i in range(0,number,1):
		print i
		a = int(random() * (max - min) + min)
		if(len(str(a))<7):
			tmp_film = "0"+str(a)
		else:
			tmp_film = str(a)
		tmp_film = "tt"+tmp_film
		try:
			x = urllib2.urlopen("http://www.omdbapi.com/?i="+tmp_film+"&plot=short&r=json").read()
			tmp.append(x)
			# print tmp
		except Exception:
			i=i-1	
	return tmp
# insere les films dans la bdd locale
def insertInDB():
	movies = downloadMovies(2)
	client = MongoClient()
	db = client.movie_db

	if(db.movie_db.count() > 0):
		db.movie_db.delete_many({})

	for i in movies:
		db.movie_db.insert(json.loads(i))

	print db.movie_db.count()
	client.close()

# verifie que le film contient les info pertinentes
def verifyMovie(movie):



insertInDB()