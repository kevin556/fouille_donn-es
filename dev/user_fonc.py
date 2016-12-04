#!/usr/bin/python2.7
# coding: utf8
'''a faire dans un shell mongodb avant de lancer les fonctions
	db.movie_db.find().forEach( function(e){ e.Rating = new Array() ;db.movie_db.save(e); });
	db.movie_db.find().forEach( function(e){ e.Looked = new Array() ;db.movie_db.save(e); });
	db.movie_db.find().forEach( function(e){ e.Looked = new Array() ;db.movie_db.save(e); });
	
'''

from pymongo import MongoClient
import random
import json
import operator


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


'''
	efface tous les utilisateurs
	n'a pas encore été testée.
	
'''

def erase_users():
	client = MongoClient()
	db = client.user_info
	db.user_info.delete_many({})
	db_movie = client.movie_db
	'''
	db_movie.movie_db.update({
	  '_id':liste_movie[i]
	},{
		'$set': {
	     'Rating': 'New Array()',
	     'Looked': 'New Array()'
		}
		}, upsert=False
	)
	Au pire a faire en manuel via un shell mongodb
	'''
	client.close()

'''
	Efface un utilisateur grace a son id,ainsi que sa présence dans la liste looked de chaque films
	
'''
def erase_user(id_user):
	client = MongoClient()
	db = client.user_info
	db_movie = client.movie_db
	tmp = client.user_info.find({'id':id_user})['Looked']
	for i in tmp:
			db_movie.movie_db.update({
				{'_id':tmp},
				{'$pull':id_user},
				{multi:true}
				})
	
	db.user_info.remove({'id':str(id_user)})
	client.close()

'''
	renvoie la liste des notes du film avec l'id id_movie
'''

def get_current_rating(id_movie):
	client = MongoClient()
	db = client.movie_db
	'''il faut apparement rajouter une colonne rating dans la base films'''
	note = db.movie_db.find_one({'_id':id_movie})['Rating']
	client.close()
	return note

'''
	renvoie la liste des utilisateurs qui ont regardé le film id_movie
'''

def get_current_looked_list(id_movie):
	client = MongoClient()
	db = client.movie_db
	note = db.movie_db.find_one({'_id':id_movie})["Looked"]
	client.close()
	return note

def modifie_base_movie(mode,liste_movie,liste_rating,id_user):
	client = MongoClient()
	db = client.movie_db
	if(mode == "liked"):
		for i in range(0,len(liste_movie),1):
			try:
				db.movie_db.update_one({
					  '_id':liste_movie[i]
				},{
  					'$push': {
				     'Rating': liste_rating[i]
				  }
				}, upsert=False)
			except Exception:
				print "add_to_rating %s"%(Exception)
	if(mode == "looked"):
		for i in range(0,1,1):
			try:
				db.movie_db.update_one({
					  '_id':liste_movie[i]
				},{
  					'$addToSet': {
				     'Looked':id_user
				  }
				}, upsert=False)
			except Exception as ex:
				template = "An exception of type {0} occured. Arguments:\n{1!r}"
				message = template.format(type(ex).__name__, ex.args)
				print message
	client.close()


'''
	fonction qui va génerer une liste de films que l'utilisateur a regardé et "liké"
	
'''

def generate_liste_movie_liked(movie_nb,id_user,min_like):
	random.seed()
	client = MongoClient()
	passed = False
	liste =[]
	liste_looked=[]
	db = client.movie_db
	tmp = db.movie_db.find({})
	nb_film = db.movie_db.count()
	for i in range(0,movie_nb,1):
		liste.append(tmp.__getitem__(random.randrange(0,nb_film,1))["_id"])
	hasard = (len(liste) - random.randrange(0,len(liste),1))+min_like
	if hasard > len(liste):
		hasard = len(liste) - 1
	for i in range(0,hasard,1):
		liste_looked.append(liste[i])
	client.close()
	return liste_looked,liste

'''
	fonction qui va generer des notes entre note_min et note_max

'''
def generate_rating(taille_liste,note_min,note_max):
	random.seed()
	liste =[]
	for i in range(0,taille_liste,1):
		liste.append(random.randrange(note_min,note_max))
	return liste

'''
	fonction qui va aller chercher dans les films des utilisateurs un nombre max_champ d'elements
	par rapport a un critere precis et renvoie une liste random avec ces éléments.
'''

def generate_favorite_(nb_max_champ,nb_film,critere):
	random.seed()
	genre =[]
	client = MongoClient()
	db = client[nom_base_movie]
	src  = db.movie_db.find({})
	i=0
	while i<nb_max_champ:
		while True:
			tmp = str(src.__getitem__(random.randrange(nb_film))[critere])
			if str(tmp) != 'N/A':
				break
		if str(tmp) not in genre :
			genre.append(str(tmp))
		i+=1	

	client.close()
	
	return genre

'''
	genere la liste des éléments majoritaires parmi les choix de l'utilisateur
'''
def get_best(nb_max_element,liste_film,critere):
	client = MongoClient()
	db = client.movie_db
	tab = {}
	liste = []
	for i in liste_film:
		tmp = db.movie_db.find_one({'_id':i})[critere]
		if tmp not in tab:
			tab[tmp]=1
		else:
			tab[tmp]+=1
	for i in range(0,nb_max_element,1):
		liste.append(sorted(tab,key = tab.get,reverse = True)[i])
	return liste
	client.close()

#genere les données random pour les utilisateurs 
def random_data(movie_nb,min_like):
	nb_champ_genre = 3
	nb_champ_country = 2
	nb_champ_year = 2
	nb_champ_language = 2
	nb_search_element = 3
	nb_best_element = 3
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
	result["liked"], result["looked"] =generate_liste_movie_liked(movie_nb,max_id,min_like)
	result["rating"] = generate_rating(len(result["liked"]),0,10);
	
	result["best_genre"] = get_best(nb_best_element,result['looked'],'Genre')
	result["best_language"]=get_best(nb_best_element,result['looked'],'Language')
	result["best_year"]=get_best(nb_best_element,result['looked'],'Year')
	result["best_actor"]=get_best(nb_best_element,result['looked'],'Genre')

	result["search_actor"]=generate_favorite_(nb_search_element,movie_nb,'Actors')
	result["search_genre"]=generate_favorite_(nb_search_element,movie_nb,'Genre')
	result["search_year"]=generate_favorite_(nb_search_element,movie_nb,'Year')
	result["search_country"]=generate_favorite_(nb_search_element,movie_nb,'Country')
	result["search_language"]=generate_favorite_(nb_search_element,movie_nb,'Language')

	result['genre']=generate_favorite_(nb_champ_genre,movie_nb,'Genre')
	result['country']=generate_favorite_(nb_champ_country,movie_nb,'Country')
	result['year']=generate_favorite_(nb_champ_year,movie_nb,'Year')
	result['language']=generate_favorite_(nb_champ_language,movie_nb,'Language')

	modifie_base_movie("liked",result["liked"],result["rating"],result["id"])
	modifie_base_movie("looked",result["liked"],result["rating"],result["id"])
	return result



#cree les utilisateurs 
def create_user(nb_user):
	client = MongoClient()
	db=client.user_info
	for i in range(0,nb_user,1):
		a = random_data(100,20)
		db.user_info.insert_one(a)
	client.close()
