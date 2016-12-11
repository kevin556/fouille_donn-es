from pymongo import MongoClient
from pie import get_data
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

# creer n utilisateurs 
# pour chaque utilisateur :
	# recuperer la liste de genre possible (en fonction des films qu'on a)
	# recuperer la liste des pays 
	# recuperer la liste des annees 
	# recuperer la liste des langues 

	# Gerer les valeurs nulles ("none")

	# 1 asssocier plusieurs (3-4) genres a chaque client et pour chaque genre tu associe une note sur 10
	#  IDEM pour pays annee langue (3-4).

def get_list_genre():

	random.seed()
	db = client[nom_base_movie]
	nb_film = db.movie_db.count()
	print nb_film
	commande = '{ "id": "'+str(random.randrange(nb_film)) +'" } '
	print commande
	genre = db.movie_db.find_one(commande)
	client.close()
	print "genre %s "%(genre)
	
	# list_genre = [];
	
	# db = client[nom_base_movie]
	# nb = db[nom_base_movie].count()
	# for i in range(0,db.movie_db.count()):
	# 	if db.movie_db.genre not in list_genre:
	# 		list_genre.append(b.movie_db.genre)
	# 	else: 
	# 		print 'in tab'
	# print max(list_genre)


	# list_genre = [];
	
	# db1 = client[nom_base_movie]
	# nb = db[nom_base_movie].count()
	# for i in range(0,nb):
	# 	if db.movie_db.genre not in list_genre:
	# 		list_genre.append(b.movie_db.genre)
	# 	else: 
	# 		print 'in tab'
	# print max(list_genre)
	# for i in range(0,list_genre.count()):
	# 	print list_genre[i]





# delete all database

# if(db.movie_db.count() > 0):
# 	db.movie_db.delete_many({})

# Affiche le nb d'element dans la base
client = MongoClient()
db= client.movie_db

# add n movie

# n=0
# while(n < 10):
# 	tmp = get_data(1)
# 	for i in tmp:
# 		db.movie_db.insert(json.loads(i))
# 	n+=1
# 	print 
# print db.movie_db.count()

get_list_genre()


client.close()












