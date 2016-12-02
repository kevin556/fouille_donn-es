#!/usr/bin/python2.7
# coding: utf8

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
	commande = '{ "id": "'+str(id_user) +'" }'
	print commande
	print db.user_info.find_one(commande)

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
	commande={}
	commande = '{ "id": "'+str(id_user) +'" } ' 
	print commande
	db.user_info.remove(commande)
	client.close()

'''genere des listes de film et ajoute l'id de la personne qui 
	a like ou dislike dans la base au niveau de la ligne du film
'''

#def modifie_base_movie():

def generate_favorite_genre():
	random.seed()
	client = MongoClient()
	db = client[nom_base_movie]
	nb_film = db.movie_db.count()
	print nb_film
	commande = '{ "id": "'+str(random.randrange(nb_film)) +'" } '
	print commande 
	genre = db.movie_db.find_one(commande)
	client.close()
	print "genre %s "%(genre)
	return genre

def generate_liste_movie_liked(movie_nb,id_user):
	random.seed()
	client = MongoClient()
	passed = False
	liste =[]
	liste_looked=[]
	db = client.movie_db
	nb_film = db.movie_db.count()
	for i in range(0,movie_nb,1):
		liste.append(random.randrange(0,nb_film,1))
	for i in range(0,len(liste)-random.randrange(0,nb_film,1),1):
		liste_looked.append(liste[i])
	return liste,liste_looked

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
	return result

def get_max_genre():
	client = MongoClient()
	maximum=0
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
	return tab,genre
	'''return tab,maximum'''
	


#cree les utilisateurs 
def create_user(nb_user):
	client = MongoClient()
	db=client.user_info
	for i in range(0,nb_user,1):
		a = random_data(100)
		db.user_info.insert_one(a)

	client.close()


