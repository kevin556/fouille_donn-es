#!/usr/bin/python2.7
from user_fonc import *
from pymongo import MongoClient

def test():
	client = MongoClient()
	db = client["movie_db"]
	print db.movie_db.count()
	tmp = db.movie_db.find({})
	print tmp.__getitem__(1)["Genre"]
	client.close()

def clean_base():
	client = MongoClient()
	db = client.movie_db
	tmp = db.movie_db.delete_many({'Response':'False'})
	tmp = db.movie_db.delete_many({'Genre':'N/A'})
	tmp = db.movie_db.delete_many({'Country':'N/A'})
	tmp = db.movie_db.delete_many({'Year':'N/A'})
	tmp = db.movie_db.delete_many({'Language':'N/A'})
	print db.movie_db.count()
	client.close()

def test_user():
	return random_data(1)
	
def test_validate():
	client = MongoClient()
	db = client.movie_db
	client.close()
'''
nb_user = get_nb_users()

erase_user(0)
for i in range(0,nb_user,1):
	show_user(i)

print generate_random_genre()

'''
# tab,genre = get_max_genre()

# print tab
# print genre

clean_base()

