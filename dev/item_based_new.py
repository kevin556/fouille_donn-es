#!/usr/bin/python2.7
# coding: utf8

from pymongo import MongoClient
import random
import json
import operator
from scipy.stats.stats import pearsonr
from user_fonc import *


nom_base_final = "user_info"
nom_base_movie = "movie_db"

# Affiche les films regarde par l'utilisateur
def getUserLookedFilms(id_user):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db

	movies = db.user_info.find_one({'id':id_user})['looked']
	for x in movies:
		print db_movies.movie_db.find_one({"_id": x})

	return movies	
# Affiche les films like/note par l'utilisateur
def getUserLikedFilms(id_user):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db

	movies = db.user_info.find_one({'id':id_user})['liked']
	for x in movies:
		print db_movies.movie_db.find_one({"_id": x})

	return movies


# recuper le film par id
def getRatingsOfMovieById(objId):
	client = MongoClient()
	db = client.movie_db
	movie = db.movie_db.find_one({"_id": objId})['Rating']
	# print movie
	return movie

def getMovieById(objId):
	client = MongoClient()
	db = client.movie_db
	movie = db.movie_db.find_one({"_id": objId})
	# print movie
	client.close()
	return movie	

# affiche nb films de la base
def show_movies(nb):
	client = MongoClient()
	db = client.movie_db
	res = db.movie_db.find()
	for doc in res:
		print(doc)

# fonction qui recuperer plusieurs films de la base et qui calcule
# le degre de correlation entre le film de l'utilisateur principal et les films recupere en base
# ex. film A et B C D 
# la fonction retourne 
	# [0.5, -1, 1]

# recupere nb films aleatoirement
def get_random_movies(nb):
	movies = []
	for x in xrange(0,nb):
		tmp = get_random_movie()
		movies.append(tmp)
		# print tmp['Rating']
		# print tmp
	return movies

# recupere un film aleatoirement depuis la base
def get_random_movie():
	client = MongoClient()
	db = client.movie_db
	res = db.movie_db.find()
	ran = random.randrange(1,db.movie_db.count(),1)
	# print res[ran]
	return res[ran]
		# for doc in res:
		# 	print(doc)

def get_













 