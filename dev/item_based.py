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
	for x in xrange(0,len(array)):
		if(array[x] == element):
			return True
	return False

# Retourne les elements communs aux deux tableaux
def get_same_element(array1, array2):
	res = []
	for x in xrange(0,len(array1)):
		for y in xrange(1,len(array2)):
			if(array1[x] == array2[y]):
				if(is_in_array(res,array1[x]) != True):
					res.append(array1[x])
	return res

# recuperer les films de l'user1
# pour tous les autres utilisateurs, recuperer celui qui a le plus de films en commun
# ajouter ces films dans same_movies
# ensuite, reparcourir le tableau et trouver le second utilisateur qui a le 
# plus de films en commun avec same_movies
# et ainsi de suite jusqu'a ce qu'il n'y ait plus d'utilisateurs qui ont des films en commun avec same_movies


def add_foreach(array1, array2):
	for x in xrange(1,len(array2)):
		array1.append(array2[x])
	return array1

# definir une fonction qui compare deux tableaux et non pas des sets
def get_movie_and_note_by_user(id_user):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db

	movies_user_p = db.user_info.find_one({'id':id_user})['liked']
	mov_rating_user_p = db.user_info.find_one({'id':id_user})['rating']

	same_movies = []
	users_used = []
	max_nb = 0
	max_user_id = -1


	# recupere l'utilisateur qui a le maximum de film en commun
	# ces films la sont mis dans
	for j in xrange(0,1500):
		if(j != id_user):
			movies_u = db.user_info.find_one({'id':j})['liked']
			mov_rating_u = db.user_info.find_one({'id':j})['rating']
			if(len(set(movies_u) & set(movies_user_p)) > max_nb):
				users_used = []
				same_movies = []
				max_nb = len(set(movies_u) & set(movies_user_p))
				users_used.append(j)
				same_movies = add_foreach(same_movies,get_same_element(movies_u,movies_user_p))
	# print users_used
	print max_nb
	print same_movies
	

	founded = True
	while(founded):
		max_nb = 0
		founded = False
		for j in xrange(0,1500):
			if(j != id_user):
				movies_u = db.user_info.find_one({'id':j})['liked']
				mov_rating_u = db.user_info.find_one({'id':j})['rating']
				if((len(set(same_movies) & set(movies_u)) > max_nb) and (is_in_array(users_used,j)) != True):
					founded = True
					max_nb = len(set(same_movies) & set(movies_u))
					users_used.append(j)
					same_movies = add_foreach(same_movies,get_same_element(same_movies,movies_u))
				# if(len(set(same_movies) & set(movies_user_p)) == 0):
		print "nombre de films ", len(same_movies)
		print "nombre d'utilisateurs " , users_used
		print "film communs trouves ", max_nb






	# print same_movies
	# print db.user_info.find_one({'id':j})
	client.close()
	return same_movies

# user p a l'id 10


# print pearsonr(x,y)
# print pearsonr(x1,y1)


# get_movie_and_note_by_user(10)
# get_movie_and_note_by_user(9)


def search_hystory(id_user):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db
	search_year = db.user_info.find_one({'id':id_user})['search_year']
	search_genre = db.user_info.find_one({'id':id_user})['search_genre']
	search_actor = db.user_info.find_one({'id':id_user})['search_actor']
	search_country = db.user_info.find_one({'id':id_user})['search_country']
	search_language = db.user_info.find_one({'id':id_user})['search_language']
	# print search_year
	# print search_genre
	# print search_country
	# print search_actor
	# print search_language
	# print search_country[0]
	newlist = []
	for i in range(0,len(search_language)):
		for j in range(0,len(search_genre)):
			for k in range(0,len(search_year)):
				for m in range(0,len(search_country)):
					listMovie = db_movies.movie_db.find({"Genre" : search_genre[j] , "Year" : search_year[k], "Language" : search_language[i] , "Country" : search_country[m]})
					for n in listMovie:
						if n['_id'] not in newlist:
							newlist.append(n['_id'])
	# for doc in newlist:
	# 	print doc
	# RECUPE HISTORY PREF AND BEST
	client.close()
	return newlist

def search_history(id_user):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db
	search_year = db.user_info.find_one({'id':id_user})['search_year']
	search_genre = db.user_info.find_one({'id':id_user})['search_genre']
	search_actor = db.user_info.find_one({'id':id_user})['search_actor']
	search_country = db.user_info.find_one({'id':id_user})['search_country']
	search_language = db.user_info.find_one({'id':id_user})['search_language']
	# print search_year
	# print search_genre
	# print search_country
	# print search_actor
	# print search_language
	# print search_country[0]
	newlist = []
	for i in range(0,len(search_language)):
		for j in range(0,len(search_genre)):
			for k in range(0,len(search_year)):
				for m in range(0,len(search_country)):
					listMovie = db_movies.movie_db.find({"Genre" : search_genre[j] , "Year" : search_year[k], "Language" : search_language[i] , "Country" : search_country[m]})
					for n in listMovie:
						if n['_id'] not in newlist:
							newlist.append(n['_id'])
	for doc in newlist:
		print doc
	# RECUPE HISTORY PREF AND BEST
	client.close()
	return newlist

def search_pref(id_user):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db
	year = db.user_info.find_one({'id':id_user})['year']
	genre = db.user_info.find_one({'id':id_user})['genre']
	country = db.user_info.find_one({'id':id_user})['country']
	language = db.user_info.find_one({'id':id_user})['language']
	newlist = []
	for i in range(0,len(language)):
		for j in range(0,len(genre)):
			for k in range(0,len(year)):
				for m in range(0,len(country)):
					listMovie = db_movies.movie_db.find({"Genre" : genre[j] , "Year" : year[k], "Language" : language[i] , "Country" : country[m]})
					for n in listMovie:
						if n['_id'] not in newlist:
							newlist.append(n['_id'])
	for doc in newlist:
		print doc
	# RECUPE HISTORY PREF AND BEST
	client.close()
	return newlist

def search_best(id_user):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db
	best_year = db.user_info.find_one({'id':id_user})['best_year']
	best_genre = db.user_info.find_one({'id':id_user})['best_genre']
	best_language = db.user_info.find_one({'id':id_user})['best_language']
	newlist = []
	for i in range(0,len(best_language)):
		for j in range(0,len(best_genre)):
			for k in range(0,len(best_year)):
				listMovie = db_movies.movie_db.find({"Genre" : best_genre[j] , "Year" : best_year[k], "Language" : best_language[i] })
				for n in listMovie:
					if n['_id'] not in newlist:
						newlist.append(n['_id'])
	for doc in newlist:
		print doc
	# RECUPE HISTORY PREF AND BEST
	client.close()
	return newlist


# get_movies_to_possible_correlation_by_nb()

# get_random_movies(3)
# create_user(2000)
# show_users(1)
search_history(1)
print "-----"
search_pref(1)
print "-----"
# for i in range(0,100):
# 	search_best(i)
search_best(1)
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


 