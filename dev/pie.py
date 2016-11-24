#!/usr/bin/python2.7
from random import * 
import urllib2

# killall -15 mongod

def get_data(number):
	tmp=[]
	max = 1000000
	min = 1
	a = 0
	tmp_film = ""
	for i in range(0,number,1):
		a = int(random() * (max - min) + min)
		if(len(str(a))<7):
			tmp_film = "0"+str(a)
		else:
			tmp_film = str(a)
		tmp_film = "tt"+tmp_film
		tmp.append(urllib2.urlopen("http://www.omdbapi.com/?i="+tmp_film+"&plot=short&r=json").read())


		print tmp[i]
	return tmp

get_data(1)