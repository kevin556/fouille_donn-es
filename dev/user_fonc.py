#!/usr/bin/python2.7
from pymongo import MongoClient

nom_base_final = "user_info"


#return max_user_id
def get_max_id():
	client = MongoClient
	db=client.user_info
	max_id = 0
	for i in range(1,db.user_info.count(),1):
		try:
			db.find("id",i)
		except Exception:
			break
	return i

def random_data():
	result =[]
	a = get_max_id()
	a = a+1
	#ville -> liste de ville dispo plus random sur la liste
	ville 


	result.append("id :"+a)
	result.append("username : user_"+a)
	result.append("ville : "+ville)
	#sexe -> random sur Homme ou Femme
	result.append("sexe : "+sexe)
	#age -> random sur un range d'age
	result.append("age : " + age)
	return result

def create_user(nb_user):
	client = MongoClient()
	db=client.user_info
	for i in range(0,nb_user,1):
		db.insert(random_data())
	db.close()


create_user(1,)

print get_max_id(nom_base_final)