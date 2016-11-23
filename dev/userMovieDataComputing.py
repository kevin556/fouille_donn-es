from pymongo import MongoClient
import json



# Calcule le pourcentage d'appartion des criteres de tout les films
# : retourne un dictionnaire ("Genre", %)
# param : type de parametre (Genre, Language etc) sauf actors
def calculate_percentages_of_criteria(user, param):
	movies = get_movies(user)
	perc_dict = DictWIthDefault("empty")
	for i in range(0,len(movies),1):
		if(perc_dict[movies[i][param]] == "empty"):
			perc_dict[movies[i][param]] = calculate_percentage_of_criteria(movies,movies[i],"Genre")
	return perc_dict

# Calcule le pourcentage d'un parametre precis
# des films que l'user a regarde
# ex. sur 100 films 50 sont des documentaires (50%)
# movies: liste des films
# name: nom du parametre 
# param: type de parametre (Genre, Year, Title etc)
def calculate_percentage_of_criteria(movies, name, param):
	res = 0
	for x in xrange(1,len(movies)):
		if(name == movies[x]["Genre"]):
			res += 1

	if res == 0:
		return 0
	else:
		return res / len(movies) * 100	

# Renvoi la(le ) (type, genre, annees) qui a le plus
# grand pourcentage d'appartion
# ex. ["Action": 80, "Comedy": 20], renverra "Action"
def get_major_by_criteria(tab, name):
	m = 0 
	gen = ""
	for x in xrange(1,len(tab)):
		if(m < tab[x][1]):
			gen = tab[x][0]
	return gen

# Pour chaque parametres correspondant, la fonction renvoi le nom/valeu
# ex. Type: movies
def get_major_criterias(user):
	params_list = ("Genre", "Type", "Year", "Country", "Language")
	maj_criterias_dict = dict()
	for param in params_list:
		maj_criterias_dict[param] = get_major_by_criteria(calculate_percentages_of_criteria(user,param))
	return maj_criterias_dict





