#!/usr/bin/python2.7
from pymongo import MongoClient

# Affiche le nb d'element dans la base
client = MongoClient()
db= client.movie_db

print db.movie_db.count()
client.close()
