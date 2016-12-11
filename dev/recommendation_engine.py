#!/usr/bin/python2.7
# coding: utf8

from pymongo import MongoClient
import random
import json
import operator
from bson import ObjectId
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

# recupere le film par ID
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

# ajoute les films de array2 qui ne sont pas encore dans array1
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
def get_common_movies_to_user(id_user):
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
			if(len(set(movies_u) & set(movies_user_p)) > max_nb):
				users_used = []
				same_movies = []
				max_nb = len(set(movies_u) & set(movies_user_p))
				users_used.append(j)
				same_movies = add_foreach(same_movies,get_same_element(movies_u,movies_user_p))
	
	founded = True
	max_users = 200
	while(founded and max_users > 0):
		max_nb = 0
		founded = False
		for j in tmp:
			if(j != id_user and j not in users_used  and max_users > 0):
				movies_u = data.__getitem__(j)['liked']
				mov_rating_u = data.__getitem__(j)['rating']
				if((len(set(same_movies) & set(movies_u)) > 6)):
					founded = True
					max_users = max_users - 1
					max_nb = len(set(same_movies) & set(movies_u))
					# print max_users
					# print max_nb
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
				# print j , x , note
				tmp = {'user_id_ref' : str(user_id_ref), 'user_id' : str(j), 'movie' : str(x), 'note' : str(note)}
				db.matrix_info.insert_one(tmp)
			else:
				"l'user n'a pas donne la note"	
	print "inserted ", db.matrix_info.count()
	client.close()
	return res

# def save_matrix_in_base(matrix, id_user):
# 	client = MongoClient()
# 	db = client.matrix_info
# 	db.matrix_info.delete_many({})
# 	for x in xrange(0,len(matrix)):
# 		tmp = str(matrix[x])
# 		db.matrix_info.insert_one(x)
# 	client.close()

# recupere la matrice existante depuis la base
def get_matrix_from_base():
	client = MongoClient()
	db = client.matrix_info
	cur = db.matrix_info.find({})
	res = []
	for doc in cur:
		print doc
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

def has_rated_movie(id_user, id_movie):
	client = MongoClient()
	db = client.user_info
	user = db.user_info.find_one({'id': id_user})
	movies = user['liked']
	print movies
	client.close()

# renvoi une liste de films qui correspond aux critere de recherche de l'utilisateur
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

# retourne une liste films qui correspondent aux preferences de l'utilisateur
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

# retourne une liste films qui se base sur le contenu majoritaire
# par ex. les genre de films qu'il a regarde le plus, les annees de sortie etc.
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

# filtre une liste de films
# ne renvoi que les films qui ont les meilleurs rating utilisateur
def search_high_rating(listMovie,nb_max_movie):
	client = MongoClient()
	db = client.user_info
	db_movies = client.movie_db
	rating_movie = []
	for i in range(0,len(listMovie)):
		note = 0
		list_rating = getRatingsOfMovieById(listMovie[i])
		for j in range(0,len(list_rating)):
			note = note + list_rating[j]
		note = note / float(len(list_rating))
		if len(rating_movie) < nb_max_movie:
			rating_movie.append([ note ,listMovie[j]])
			rating_movie.sort()
		elif rating_movie[0][0] < note:
			del rating_movie[0]
			rating_movie.append([note , listMovie[j]])
			rating_movie.sort()
	client.close()
	return rating_movie



# permet de savoir si le film "movie" a ete regarde par l'utilisateur dans la matrice
def seen(id_user,movie,matrix):
	res = False
	for x in matrix:
		if(x['user_id'] == id_user):
			if(movie == x['movie']):
				res = True
				break
	return res			

# renvoi la note donnee par l'utilisateur au film "movie"
def get_note(id_user,movie,matrix):
	for x in matrix:
		if(x['user_id'] == id_user):
			if(movie == x['movie']):
				return x['note']



# garde que les film regardes par tout le monde
def filter_matrix(matrix):
	movies = []
	users = []
	notes = []
	for x in matrix:
		movies.append(x['movie'])
		users.append(x['user_id'])
		notes.append(x['note'])
	print users

	mat_filtered = []
	tmp_u = []
	for u in users:
		tmp = []
		if u not in tmp_u:
			tmp_u.append(u)
			for m in movies:
				if(seen(u,m,matrix)) == True:
					if m not in tmp:
						tmp.append(m)
						mat_filtered.append((u,m,get_note(u,m,matrix)))
						# print "seen" , u , " ", m
				else:
					if m not in tmp:
						tmp.append(m)
						mat_filtered.append((u,m,random.randrange(1,10)))
	print mat_filtered					
	return mat_filtered

# retourne les rating du film a partir de la matric
def get_ratings_from_matrix(id_movie, matrix):
	rates = []
	for x in matrix:
		if id_movie == x[1]:
			rates.append(x[2])
	# print rates		
	return rates		

# fonction qui converti un tableau contenant des string en tableau contenant des int
def aux_fun(tab):
	res = []
	for x in tab:
		res.append(int(x))
	return res	

# sauvegarde en base les donnés de correlation
def save_correlation_information(movie_corr):
	client = MongoClient()
	db = client.matrix_correlation
	db.matrix_correlation.delete_many({})

	for x in movie_corr:		
		tmp = {'id_user' : x[0],'id_movie': x[1], 'corr': x[2], "id_ref_movie" : x[3]}
		db.matrix_correlation.insert_one(tmp)
	client.close()	

# retourne le film qui a la meilleure correlation
# avec le film passe en parametre
def calculate_corelations_between_movies(matrix):
	print "calcule de degre de correlation"
	tmp = []
	for x in matrix:
		if x[1] not in tmp:
			tmp.append(x[1])


	id_movie = tmp[random.randrange(0,len(tmp))]
	print "choosen movie" , id_movie
	print id_movie
	movie_ref_ratings = []
	movies = []
	movie_corr = []
	for x in matrix:
		if(x[1] == id_movie):
			movie_ref_ratings = get_ratings_from_matrix(id_movie,matrix)
			movie_ref_ratings = aux_fun(movie_ref_ratings)
			break

	used_movies = []
	for x in matrix:
		if(x not in used_movies):
			used_movies.append(x)
			if x != id_movie:
				one = get_ratings_from_matrix(x[1],matrix)
				one = aux_fun(one)
				# print len(one) , " " , len(movie_ref_ratings)
				movie_corr.append((x[0],x[1],pearsonr(one,movie_ref_ratings),id_movie))

	print movie_corr
	save_correlation_information(movie_corr)

# item-base model
def get_best_movie_by_corelation():
	print "Item-Based: recherche des films a recommander"
	client = MongoClient()
	db = client.matrix_correlation
	res = db.matrix_correlation.find({})
	print "film de reference: " , res[0]['id_ref_movie']
	print "recherche du film qui possede la meilleure correlation..."

	max_cor = 0
	movie_id = 0
	for x in res:
		if x['corr'][0] > max_cor:
			if x['id_movie'] != x['id_ref_movie']:
				max_cor = x['corr'][0]
				movie_id = x['id_movie']
	print "film possedant la meilleure correlation = " , movie_id , " qui est de " , max_cor
	

	db = client.movie_db
	oid_str = movie_id
	oid2 = ObjectId(oid_str)
	result = db.movie_db.find_one({"_id": oid2})


	print result
	client.close()	

# renvoi un film random qui a ete like par l'utilisateur
def get_random_movie_from_user(id_user):
	client = MongoClient()
	db = client.user_info
	res = db.user_info.find_one({'id': id_user})
	x = random.randrange(0,len(res['liked']))
	movie = res['liked'][x]
	client.close()
	return movie



# user-based
def get_notes_given_by_main_user():
	print "User-Based: recherche des films a recommander"
	matrix = get_matrix_from_base()
	movies_used = []
	corr = []
	notes = []
	users_used = []

	user_main_notes = []
	for x in matrix:
		if x['movie'] not in movies_used:
			movies_used.append(x['movie'])
			user_main_notes.append(get_note_to_film_by_user_id(x['movie'],10))
	# print user_main_notes			

	tmp = []
	for u in matrix:
		tmp = []
		if(u['user_id'] not in users_used):
			movies_used = []
			for x in matrix:
				if x['movie'] not in movies_used:
					movies_used.append(x['movie'])
					# print x['movie'], " " , u['user_id']
					if get_note(x['movie'],u['user_id'],matrix) == None:
						tmp.append(random.randrange(0,10))
						# print tmp
			# print len(user_main_notes) , " " , len(tmp)
			# print pearsonr(user_main_notes,tmp)
			corr.append((u['user_id'],pearsonr(user_main_notes,tmp)[0]))
	# print corr

	max_corr = 0
	user_max_cor = -1
	for x in corr:
		if x[1] > max_corr:
			max_corr = x[1]
			user_max_cor = x[0]
	print "correlation = ", max_corr	," user max id = " , user_max_cor

	client = MongoClient()
	db = client.movie_db
	oid2 = ObjectId(get_random_movie_from_user(int(user_max_cor)))
	result = db.movie_db.find_one({"_id": oid2})
	print "le film a proposer est ", result


# gerenation de la matrice pour l'user dont l'id est egal a 10
id_user = 10
# movies_users = get_common_movies_to_user(id_user)
# print (movies_users[0])
# print (movies_users[1])
# print len(movies_users[0])
# creation de la matrice et sauvegarde en base
# matrix = make_matrix(id_user,movies_users[0],movies_users[1])
matrix = get_matrix_from_base()
# # garde que les film regardes par tout le monde
matrix = filter_matrix(matrix)

calculate_corelations_between_movies(matrix)
# item-based model
get_best_movie_by_corelation()
# user-based model
get_notes_given_by_main_user()



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
# 	[B, D] (ceux qui ont la correlation la meilleures correlation avec le film A)



# fonction qui retourne n films qui ont la parfaite meilleures correlation avec les films de l'utilisateur
# ex. film A B C et E F G H 
#  la fonction retourne [F, H] (ne pas prendre en compte les degres de correlation tres bas) 


 