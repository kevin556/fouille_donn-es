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

# filtre les films passes en paramètre et renvoi les films possible
# pour le calcul de degre de correlation
# movies: liste de films recuperes en base
# movie: un film de l'utilisateur principale
def get_movies_to_possible_correlation(movies, movie):
	filtered_movies = []
	# print 'in get_movies_to_possible_correlation___________________'
	for x in movies:
		rating = x['Rating']

		# print "movie's likes: ", len(rating)
		# print "user's movie likes ", len(movie)
		# print(len(rating) , len(movie))
		if(len(rating) == len(movie['Rating'])):
			filtered_movies.append(x)
			# print rating
			# print 

	return filtered_movies		

# Renvoi (nb) films qui ont la meuilleures correlation
# movies: liste de films
# movie: film de reference
# 
def get_correlation_movies(movies, movie):
	cor_list = []
	movies_list = []
	for x in movies:
		cor_list.append(get_correlation(x,movie)[0])
		movies_list.append(x)
	print cor_list

	# #recuperons les nb meilleurs
	# correls = []
	# for x in cor_list:
	# 	correls.append(x[0])

	# affiche le deg de correlation
	print max(cor_list)
	print cor_list
	# affiche le film
	# print cor_list.index[max(cor_list)]


# calcul le degre de correlation entre deux films
# movie1: film choisi aleatoirement 
# movie2: film de l'utilisateur
def get_correlation(movie1,movie2):
	rating_movie_ref = movie2['Rating']
	rating_movie = movie1['Rating']
	res = pearsonr(rating_movie_ref,rating_movie)
	# print res
	return res


# pour un utilisateur donne
# selectionne (aleatoirement) un film que l'utilisateur a note (recupere les rating du film)
# renvoi les films de la base qui av
def get_movies_to_possible_correlation_by_nb(nb,user_id):
	print "get_movies_to_possible_correlation_by_nb: Filtering movies"
	movies_user = getUserLikedFilms(user_id)
	user_movie_test = movies_user[len(movies_user) - 1]
	user_movie = getMovieById(user_movie_test)
	movies_filtered = []
	while(len(movies_filtered) <= nb):
		movies_random = get_random_movies(100)
		movies_filtered = get_movies_to_possible_correlation(movies_random, user_movie)
	print 'Moviesss------'
	for x in movies_filtered:
		print x['Rating']
	get_correlation_movies(movies_filtered,user_movie)


	# print (len(movies_filtered))
		


# get_movies_to_possible_correlation_by_nb(10,9)

def get_note_given_by_user(id_user, id_movie):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db

	movies = db.user_info.find_one({'id':id_user})['liked']
	mov_rating = db.user_info.find_one({'id':id_user})['rating']

	x = movies.index(id_movie)
	# print id_movie
	print "la note donne est " , mov_rating[x]
	# print mov_rating
	return mov_rating[x]
	client.close()

# get_note_given_by_user(9)

# renvoi true si l'element est dans l'array
def is_in_array(array,element):
	for x in array:
		if(x == element):
			return true
	return false

# Retourne les elements communs aux deux tableaux
def get_same_element(array1, array2):
	res = []
	for x in array1:
		for y in array2:
			if(array1[x] == array2[y]):
				if(isInArray() != true):
					res.append(array1[x])
	return res

# recuperer les films de l'user1
# pour tous les autres utilisateurs, recuperer celui qui a le plus de films en commun
# ajouter ces films dans same_movies
# ensuite, reparcourir le tableau et trouver le second utilisateur qui a le 
# plus de films en commun avec same_movies
# et ainsi de suite jusqu'a ce qu'il n'y ait plus d'utilisateurs qui ont des films en commun avec same_movies





# definir une fonction qui compare deux tableaux et non pas des sets
def get_movie_and_note_by_user(id_user):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db

	movies = db.user_info.find_one({'id':id_user})['liked']
	mov_rating = db.user_info.find_one({'id':id_user})['rating']
	# for x in xrange(1,len(movies)):
	# 	print db_movies.movie_db.find_one({"_id": movies[x]})['_id']
	# 	print mov_rating[x]
	# cherche les films commun pour un certain nombre d'utilisateurs
	movies_big = []
	movies_rate_big = []


	same_movies = []
	for j in xrange(1,1000):
		movies1 = db.user_info.find_one({'id':j})['liked']
		mov_rating1 = db.user_info.find_one({'id':j})['rating']
		
		if(len(same_movies) == 0):
			if(len(set(movies) & set(movies1)) > 4):
				same_movies.append(set(movies) & set(movies1))
				print "debut"
		else:
			if(len(set(same_movies) & set(movies1)) > 3):
				same_movies.append(set(movies) & set(movies1))
				print "ici"
	print same_movies

	client.close()
	return movies


# get_movie_and_note_by_user(9)






# get_movies_to_possible_correlation_by_nb()

# get_random_movies(3)
# create_user(2000)
# show_users(10)
# getUserLookedFilms(9)
# getFilmByObjectId()



# fonction qui recuper un nombre n de films en base


# fonction qui retourne la liste des ids de films qui ont une parfaite correlation avec le film de l'utilisateur
# ex. film A et B C D
# la fonction retourne
	# [B, D] (ceux qui ont la correlation la meilleures correlation avec le film A)



# fonction qui retourne n films qui ont la parfaite meilleures correlation avec les films de l'utilisateur
# ex. film A B C et E F G H 
 # la fonction retourne [F, H] (ne pas prendre en compte les degres de correlation tres bas) 


 