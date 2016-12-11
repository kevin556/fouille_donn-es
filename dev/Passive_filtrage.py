from pymongo import MongoClient
import random
import json

nom_base_final = "user_info"
nom_base_movie = "movie_db"



# generation de l'activite de l'utilisateur
 # pour chaque user:
 	# recuper 100 films pour chaque utilisateurs (sans doublons)
 	# Dans l'utilisateur:
		# pour chaque user sauvegarder 70 films_notes:{ id_film: note (7/10)} 
		# pour chaque user sauvegarder 30 films_notes:id_film}
	# Dans le film:
		"""movies{
			id10:
				note: 6/10
				nbPersonnesNotes: 100
				nbPersonnesRegarde: 200
								}"""