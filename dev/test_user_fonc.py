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
	tmp = db.movie_db.delete_many({'Country':'N/A'})
	tmp = db.movie_db.delete_many({'Language':'N/A'})
	tmp = db.movie_db.delete_many({'Genre':'N/A'})
	tmp = db.movie_db.delete_many({'Year':'N/A'})
	print tmp.deleted_count
	client.close()


def test_user():
	return random_data(1)
	

def test_validate():
	client = MongoClient()
	db = client.movie_db
	client.close()

'''
tab,genre,liste = get_max_genre()
clean_base()
print tab
print genre
print liste
'''
# create_user(1)