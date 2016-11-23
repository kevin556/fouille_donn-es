from pymongo import MongoClient
import json



# Calcule le pourcentage des genre de tout les films
# : retourne un dictionnaire ("Genre", %)
def calculate_percentage_genres(user):
	movies = get_movies(user)
	perc_dict = DictWIthDefault("empty")
	for i in range(0,len(movies),1):
		if(perc_dict[movies[i]["Genre"]] == "empty"):
			perc_dict[movies[i]["Genre"]] = calculate_percentage_of_criteria(movies,movies[i],"Genre")
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




		
