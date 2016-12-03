#!/usr/bin/python2.7
# coding: utf8
'''a faire dans un shell mongodb avant de lancer les fonctions
	db.movie_db.find().forEach( function(e){ e.Rating = new Array() ;db.movie_db.save(e); });
	db.movie_db.find().forEach( function(e){ e.Looked = new Array() ;db.movie_db.save(e); });

'''

from pymongo import MongoClient
import random
import json

nom_base_final = "user_info"
nom_base_movie = "movie_db"

#retourne le nombre de films dans la base.
def get_nb_max_movie():
	client = MongoClient()
	db = client[nom_base_movie]
	nb = db[nom_base_movie].count()
	client.close()
	return nb

#donne le nombre d'utilisateurs.
def get_nb_users():
	client = MongoClient()
	db = client[nom_base_final]
	nb_user = db[nom_base_final].count()
	print nb_user
	return nb_user
	client.close()

#affiche tous les utilisateurs
def show_users():
	client = MongoClient()
	db = client.user_info
	print db.user_info.find({})
	client.close()
	
#affiche un utilisateur en particulier
def show_user(id_user):
	client = MongoClient()
	db = client.user_info
	print db.user_info.find_one({'id':id_user})

#retourne le nombre d'utilisateurs dans la table user_id
def get_max_id():
	client = MongoClient()
	db=client.user_info
	max_id = db.user_info.count()
	try:
		db.find("id",max_id+1)
		client.close()
		return max_id+1
	except Exception:
		client.close()
		return max_id


#efface tous les utilisateurs
def erase_users():
	client = MongoClient()
	db = client.user_info
	db.user_info.delete_many({})
	client.close()

#efface un utilisateur grace a son id.
def erase_user(id_user):
	client = MongoClient()
	db = client.user_info
	db.user_info.remove({'id':str(id_user)})
	client.close()

'''genere des listes de film et ajoute l'id de la personne qui 
	a like ou dislike dans la base au niveau de la ligne du film
'''

def get_current_rating(id_movie):
	client = MongoClient()
	db = client.movie_db
	'''il faut apparement rajouter une colonne rating dans la base films'''
	note = db.movie_db.find_one({'_id':id_movie})['Rating']
	print note
	client.close()
	return note

def get_current_looked_list(id_movie):
	client = MongoClient()
	db = client.movie_db
	note = db.movie_db.find_one({'_id':id_movie})["Looked"]
	print note
	client.close()
	return note

def modifie_base_movie(mode,liste_movie,liste_rating,id_user):
	client = MongoClient()
	db = client.movie_db
	data = db.movie_db.find({})
	if(mode == "liked"):
		for i in range(0,1,1):
			id_movie = data.__getitem__(liste_movie[i]).get('_id')
			print id_movie
			print "film %d note %d \n"%(liste_movie[i],liste_rating[i])
			try:
				tmp = db.movie_db.update_one({
					  '_id':id_movie
				},{
  					'$push': {
				     'Rating': liste_rating[i]
				  }
				}, upsert=False)
				'''
				print tmp.modified_count
				print tmp.matched_count
				print tmp.raw_result
				'''
			except Exception:
				print "add_to_rating %s"%(Exception)
	if(mode == "looked"):
		for i in range(0,1,1):
			id_movie = data.__getitem__(liste_movie[i]).get('_id')
			try:
				get_current_looked_list(id_movie)
				tmp = db.movie_db.update_one({
					  '_id':id_movie
				},{
  					'$addToSet': {
				     'Looked':id_user
				  }
				}, upsert=False)
				print tmp.modified_count
				print tmp.matched_count
				print tmp.raw_result

			except Exception as ex:
				template = "An exception of type {0} occured. Arguments:\n{1!r}"
				message = template.format(type(ex).__name__, ex.args)
				print message

	get_current_rating(id_movie)
	get_current_looked_list(id_movie)
	client.close()

def generate_favorite_genre():
	random.seed()
	client = MongoClient()
	db = client[nom_base_movie]
	nb_film = db.movie_db.count()
	src  = db.movie_db.find({})
	genre = src.__getitem__(random.randrange(nb_film))['Genre']
	client.close()
	print "genre %s "%(genre)
	return genre

def generate_liste_movie_liked(movie_nb,id_user,min_like):
	random.seed()
	client = MongoClient()
	passed = False
	liste =[]
	liste_looked=[]
	db = client.movie_db
	nb_film = db.movie_db.count()
	for i in range(0,movie_nb,1):
		liste.append(random.randrange(0,nb_film,1))
	
	hasard = (len(liste) - random.randrange(0,len(liste),1))+min_like
	if hasard > len(liste):
		hasard = len(liste)
	for i in range(0,hasard,1):
		liste_looked.append(liste[i])
	client.close()
	print liste_looked,liste
	return liste_looked,liste

def generate_rating(taille_liste,note_min,note_max):
	random.seed()
	liste =[]
	for i in range(0,taille_liste,1):
		liste.append(random.randrange(note_min,note_max))
	return liste

#genere les données random pour les utilisateurs 
def random_data(movie_nb):
	random.seed()
	liste_ville= ["paris","lyon","toulouse","marseille","nice","nantes","strasbourg"];
	liste_sexe=["Homme","Femme"]
	max_id = get_max_id()
	max_movie_nb = get_nb_max_movie()
	b = random.randrange(0,len(liste_ville),1)
	c = random.randrange(0,len(liste_sexe),1)
	result ={}
	result['id']=max_id
	result['username']="user_"+str(max_id)
	result['ville']=liste_ville[b]
	result['genre']=generate_favorite_genre()
	#sexe -> random sur Homme ou Femme
	result['sexe']=liste_sexe[c]
	#age -> random sur un range d'age
	result['age']=random.randrange(13,120,1)
	result["liked"], result["looked"] =generate_liste_movie_liked(movie_nb,max_id)
	result["rating"] = generate_rating(len(result["liked"]),0,10);
	modifie_base_movie("liked",result["liked"],result["rating"],result["id"])
	modifie_base_movie("looked",result["liked"],result["rating"],result["id"])
	return result

def get_max_genre():
	client = MongoClient()
	maximum=0
	liste_type = []
	genre =""
	db = client["movie_db"]
	src = db.movie_db.find({})
	tab ={}
	tmp = ""
	for j in range(1,1000,1):
		tmp ="'" + src.__getitem__(j)['Genre'] + "'"
		if tmp not in tab:
			tab[tmp]=1
		else:
			tab[tmp]+=1
	for j in tab:
		print tab[j]
		maximum = max(int(tab[j]),maximum)
		if(maximum == int(tab[j])):
			genre = j
	for k in tab:
		liste_type.append(k)
	print liste_type
	client.close()
	return tab,genre,liste_type
	'''return tab,maximum'''

#cree les utilisateurs 
def create_user(nb_user):
	client = MongoClient()
	db=client.user_info
	for i in range(0,nb_user,1):
		a = random_data(100)
		db.user_info.insert_one(a)
	client.close()
