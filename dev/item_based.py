#!/usr/bin/python2.7
# coding: utf8

from pymongo import MongoClient
import random
import json
import operator


nom_base_final = "user_info"
nom_base_movie = "movie_db"


# fonction qui recuperer plusieurs films de la base et qui calcule
# le degre de correlation entre le film de l'utilisateur principal et les films recupere en base
# ex. film A et B C D 
# la fonction retourne 
	# [0.5, -1, 1]


# fonction qui recuper un nombre n de films en base


# fonction qui retourne la liste des ids de films qui ont une parfaite correlation avec le film de l'utilisateur
# ex. film A et B C D
# la fonction retourne
	# [B, D] (ceux qui ont la correlation la meilleures correlation avec le film A)



# fonction qui retourne n films qui ont la parfaite meilleures correlation avec les films de l'utilisateur
# ex. film A B C et E F G H 
 # la fonction retourne [F, H] (ne pas prendre en compte les degres de correlation tres bas) 

 