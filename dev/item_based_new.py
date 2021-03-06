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
				if(array1[x] not in res):
				# if(is_in_array(res,array1[x]) != True):
					res.append(array1[x])
	return res

# recuperer les films de l'user1
# pour tous les autres utilisateurs, recuperer celui qui a le plus de films en commun
# ajouter ces films dans same_movies
# ensuite, reparcourir le tableau et trouver le second utilisateur qui a le 
# plus de films en commun avec same_movies
# et ainsi de suite jusqu'a ce qu'il n'y ait plus d'utilisateurs qui ont des films en commun avec same_movies


def add_foreach(array1, array2):
	for x in xrange(0,len(array2)):
		if array2[x] not in array1:
			array1.append(array2[x])
			# print "pas dedans"
		# else:
			# print "dedans"
	return array1



# testons la fonction au dessus
def test_get_note_to_film_by_user_id(id_user):
	client = MongoClient()
	db = client.user_info
	data = db.user_info.find_one({'id':id_user})
	for i in xrange(0,len(data['looked'])):
		get_note_to_film_by_user_id(data['looked'][i],id_user)
	client.close()





# get_note_to_film_by_user_id('58371092256a1a046d47f9d5',22)
# get_note_to_film_by_user_id('58371180256a1a046d47fc4c',22)
# test_dessus(55)
# definir une fonction qui compare deux tableaux et non pas des sets
# stocke les utilisateurs qui ont les films en commun afin de ne pas tous les reparcouri
# phase 1
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
	data = db.user_info.find({})

	# recupere l'utilisateur qui a le maximum de film en commun
	# ces films la sont mis dans
	tmp = []

	for j in xrange(0,1500):
		if(j != id_user):
			movies_u = data.__getitem__(j)['liked']
			mov_rating_u = data.__getitem__(j)['rating']
			if len(set(movies_u) & set(movies_user_p)) > 0 and j not in tmp:
				tmp.append(j)
			if(len(set(movies_u) & set(movies_user_p)) == 5):
				users_used = []
				same_movies = []
				max_nb = len(set(movies_u) & set(movies_user_p))
				users_used.append(j)
				same_movies = add_foreach(same_movies,get_same_element(movies_u,movies_user_p))
	'''
	print tmp
	# print users_used
	print max_nb
	print same_movies
	'''
	founded = True
	while(founded):
		max_nb = 0
		founded = False
		for j in tmp:
			if(j != id_user and j not in users_used):
				movies_u = data.__getitem__(j)['liked']
				mov_rating_u = data.__getitem__(j)['rating']
				if((len(set(same_movies) & set(movies_u)) == 5)):
					founded = True
					max_nb = len(set(same_movies) & set(movies_u))
					print max_nb
					users_used.append(j)
					same_movies = add_foreach(same_movies,get_same_element(same_movies,movies_u))
				# if(len(set(same_movies) & set(movies_user_p)) == 0):
	print "nombre de films ", len(same_movies)
	print "utilisateurs " , users_used
	# print same_movies
	# print db.user_info.find_one({'id':j})
	client.close()
	return same_movies, users_used






# cree la matrice pour chaque film:
# [id_film, note][j]
# id_user_ref: user de references
def make_matrix(user_id_ref, movies, users):
	client = MongoClient()
	db = client.matrix_info
	db.matrix_info.delete_many({})
	print len(movies)
	res = []
	for x in movies:
		for j in users:
			note = get_note_to_film_by_user_id(x,j)
			if(note != None):
				print j , x , note
				tmp = {'user_id_ref' : str(user_id_ref), 'user_id' : str(j), 'movie' : str(x), 'note' : str(note)}
				db.matrix_info.insert_one(tmp)
			else:
				"l'user n'a pas donne la note"	
	print "inserted ", db.matrix_info.count()
	client.close()
	return res	

def save_matrix_in_base(matrix, id_user):
	client = MongoClient()
	db = client.matrix_info
	db.matrix_info.delete_many({})
	for x in xrange(0,len(matrix)):
		tmp = str(matrix[x])
		# db.matrix_info.insert_one(x)
	client.close()

# recupere la matrice existante depuis la base
def get_matrix_from_base():
	client = MongoClient()
	db = client.matrix_info
	cur = db.matrix_info.find({})
	res = []
	for doc in cur:
		# print doc
		res.append(doc)
	# print res
	client.close()
	return res



# renvoi la note du film donnee par l'utilisateur
def get_note_to_film_by_user_id(id_film,id_user):
	client = MongoClient()
	db = client.user_info
	# print "id du film ", id_film
	# print "id de l'user ", id_user
	tmp = db.user_info.find_one({'id':id_user})
	#print tmp
	compteur = 0
	for i in tmp['liked']:
		#print "yo %s "%(i)
		if str(i) == str(id_film):
			# print i
			# print compteur
			client.close()
			# print tmp['rating'][compteur]
			return tmp['rating'][compteur]
		# else:
			# print "le film:",str(i), " n'as pas ete note"  	
		compteur +=1	
	# print "erreur le film n'est pas present"
	client.close()


def get_rates_for_all_movies(matrix):
	ratings = []
	used_movies = []
	for x in matrix:
		if(x['movie'] not in used_movies):
			used_movies.append(x['movie'])
			ratings.append((x['movie'],get_all_rates_for_movie(x['movie'],matrix)))


	for x in ratings:
		print len(x[1])
	return ratings	


def get_all_rates_for_movie(id_movie, matrix):
	rating = []
	compteur = 0
	for x in matrix:
		if id_movie == x['movie']:
			rating.append(x['note'])
			compteur = compteur +1
	return rating
		


def get_noted_from_mat(user_id,matrix):
	for x in matrix:
		if x['user_id'] == user_id:
			print x['movie']


# renvoi l'user qui a le plus de film en commun
def get_user_max_common_film(matrix):
	client = MongoClient()
	db = client.user_info
	user_ids = []
	for x in matrix:
		user_ids.appen(x['user_id'])

	showed = []
	for x in user_ids:
		if x not in showed:
			print x , " apparait " , user_ids.count(x), " fois"
	client.close()



# gerenation de la matrice pour l'user dont l'id est egal a 10
movies_users = get_movie_and_note_by_user(10)
print (movies_users[0])
print (movies_users[1])
print len(movies_users[0])
matrix = make_matrix(10,movies_users[0],movies_users[1])
save_matrix_in_base(matrix,10)

matrix = get_matrix_from_base()
get_common_movies(matrix)




# user p a l'id 10
# x = [9,10,18,2]
# y = [9,10,18,1]

# x1 = [209,210,211,212]
# y1 = [209,210,211,211]


# print pearsonr(x,y)
# print pearsonr(x1,y1)


# get_movie_and_note_by_user(10)
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


 