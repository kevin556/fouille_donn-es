#!/usr/bin/python2.7
# coding: utf8

from pymongo import MongoClient
import random
import json

nom_base_final = "user_info"


#retourne le nombre de films dans la base.
def get_nb_max_movie():
	client = MongoClient()
	db = client.movie_db
	nb = db.movie_db.count()
	client.close()
	return nb


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
'''
def erase_user(id_user):
	client = MongoClient()
	db = client.user_info
	commande={}
	commande = '{"id " : ' + '"' + str(id_user) + '"}'
	print commande
	db.user_info.delete_many(commande)
	client.close()
'''

'''genere des listes de film et ajoute l'id de la personne qui 
	a like ou dislike dans la base au niveau de la ligne du film
'''

def generate_liste_movie_liked(movie_nb,mode,id_user):
	random.seed()
	client = MongoClient()
	passed = False
	liste =[]
	db = client.movie_db
	nb_film = db.movie_db.count()
	for i in range(0,movie_nb,1):
		liste.append(random.randrange(0,nb_film,1))
	print liste
	print mode

	if(str(mode) == str(1)):
		commande = 'like' +"':"  + str(id_user)+"'"
		passed = True
	if(str(mode) == str(-1)):
		commande = "'dislike' : " + str(id_user) 
		passed = True
	if not passed :
		print "erreur deuxieme argument"
		return 

	for i in liste:
		db.movie_db.update({
			'id':str(liste)
			},{
				'$set':{
					commande
				}
			}
			,upsert=False)

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
	#sexe -> random sur Homme ou Femme
	result['sexe']=liste_sexe[c]
	#age -> random sur un range d'age
	result['age']=random.randrange(13,120,1)
	result["like"]=generate_liste_movie_liked(movie_nb,"1",max_id)
	result["dislike"]=generate_liste_movie_liked(movie_nb,"-1",max_id)
	return result


#cree les utilisateurs 
def create_user(nb_user):
	client = MongoClient()

	db=client.user_info
	for i in range(0,nb_user,1):
		a = random_data(100)
		db.user_info.insert_one(a)

	client.close()

create_user(1)

'''erase_user(1)'''

