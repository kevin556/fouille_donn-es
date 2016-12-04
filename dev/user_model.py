#!/bin/bash/python2.7
#coding:utf-8
'''
	Pour le user model.
	On analyse les ressemblances entre les utilisateurs afin de realiser un premier tri.
	Puis on repére les utilisateurs qui ont regardé au moins les mêmes films que l'utilisateur principal.
	Enfin on parse dans les listes des utilisateurs le ou les films majoritaires et on le ou les propose à l'utilisateur courant.
'''

'''
	from scipy.stats import personr
'''
from scipy.stats.stats import pearsonr 
from pymongo import MongoClient

'''
	fonction qui calcule le degré de correlation sur la liste de film
'''

def make_matrice_correlation_by_criteria(criteria):
	client = MongoClient()
	db_matrice = client.matrice_correlation_user
	db_user = client.user_info
	src = db_user.user_info.find({})
	for i in range(0,db_user.user_info.count(),1):
		id_usr = src.__getitem__(i)['id']
		user_to_compare = db_user.user_info.find_one({'id':id_usr})
		for j in range(i,db_user.user_info.count(),1):
			user_tmp = db_user.user_info.find_one({'id':src.__getitem__(j)['id']})
			db_matrice.matrice_correlation_user[i].append(pearsonr(user_to_compare,user_tmp))
	client.close()

def get_group_of_user(user_to_compare):
	client = MongoClient()
	print user_to_compare

	client.close()