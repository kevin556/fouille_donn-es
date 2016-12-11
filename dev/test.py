#!/usr/bin/python2.7
from pymongo import MongoClient

client= MongoClient()
db = client.movie_db

print db.movie_db.count()
client.close()
