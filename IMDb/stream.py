import streamlit as st
from pymongo import MongoClient
import pymongo
import pandas as pd
from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé d'API Atlas à partir des variables d'environnement
ATLAS_KEY = os.getenv('ATLAS_KEY')

# Se connecter à la base de données IMDb dans Atlas
client = MongoClient(ATLAS_KEY)
db = client["bdd"]
collection = db["top_imdb"]


# Sidebar pour sélectionner l'onglet
onglet = st.sidebar.selectbox("Choisissez un onglet", ["question", "recherche"])


if onglet == "question":

    # Trouver le document correspondant au film le plus long
    longest_movie = collection.find_one(sort=[("duree", pymongo.DESCENDING)])

    # Afficher le titre et la durée du film le plus long
    st.header("Q1 : Quel est le film le plus long")
    st.write("Le film le plus long est '", longest_movie["titre"], "' avec une durée de", longest_movie["duree"], "minutes.")

    st.header("Q2 : Quels sont les 5 films les mieux notés ?")
    st.write("Les 5 films les mieux notés :")
    best_movies = collection.find().sort("score", pymongo.DESCENDING).limit(5)
    df_best_movies = pd.DataFrame(list(best_movies))
    st.write(df_best_movies[["titre", "score"]])


    st.header("Q3: Dans combien de films a joué Morgan Freeman ? Tom Cruise ?")

    # Compter le nombre de films dans lesquels Morgan Freeman a joué
    num_morgan_freeman = collection.count_documents({"acteurs": {"$regex": "Morgan Freeman"}})

    # Compter le nombre de films dans lesquels Tom Cruise a joué
    num_tom_cruise = collection.count_documents({"acteurs": {"$regex": "Tom Cruise"}})

    # Afficher les résultats dans Streamlit
    st.write("Morgan Freeman a joué dans", num_morgan_freeman, "films.")
    st.write("Tom Cruise a joué dans", num_tom_cruise, "films.")

    st.header("Q4: Quels sont les 3 meilleurs films d’horreur ? Dramatique ? Comique ?")


    # Récupérer les 3 meilleurs films d'horreur
    best_horror = collection.find({"genre": {"$regex": "Horror"}}, sort=[("score", pymongo.DESCENDING)], limit=3)
    st.write("Les 3 meilleurs films d'horreur :")

    for film in best_horror:
        st.write(film["titre"], "(", film["score"], ")")

    # Récupérer les 3 meilleurs films dramatiques
    best_drama = collection.find({"genre": {"$regex": "Drama"}}, sort=[("score", pymongo.DESCENDING)], limit=3)
    st.write("Les 3 meilleurs films dramatiques :")
    for film in best_drama:
        st.write(film["titre"], "(", film["score"], ")")

    # Récupérer les 3 meilleurs films comiques
    best_comedy = collection.find({"genre": {"$regex": "Comedy"}}, sort=[("score", pymongo.DESCENDING)], limit=3)
    st.write("Les 3 meilleurs films comiques :")
    for film in best_comedy:
        st.write(film["titre"], "(", film["score"], ")")
        
        
    st.header("Q5: Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?")

    # Récupérer les 100 films les mieux notés
    top_movies = collection.find().sort("score", pymongo.DESCENDING).limit(100)

    # Initialiser les compteurs pour chaque nationalité
    total_movies = 0
    us_movies = 0
    fr_movies = 0

    # Parcourir les films et compter le nombre de films de chaque nationalité
    for movie in top_movies:
        total_movies += 1
        if "United States" in movie["pays"]:
            us_movies += 1
        elif "France" in movie["pays"]:
            fr_movies += 1

    # Calculer les pourcentages correspondants
    us_percentage = us_movies / total_movies * 100
    fr_percentage = fr_movies / total_movies * 100

    # Afficher les résultats
    st.write("Parmi les 100 films les mieux notés :")
    st.write("- {0:.2f}% sont américains".format(us_percentage))
    st.write("- {0:.2f}% sont français".format(fr_percentage))


    st.header("Q6: Quel est la durée moyenne d’un film en fonction du genre ?")


    # Calculer la durée moyenne d'un film en fonction de son genre
    pipeline = [
        {"$group": {"_id": "$genre", "duree_moyenne": {"$avg": "$duree"}}},
        {"$sort": {"_id": 1}}
    ]
    resultats = collection.aggregate(pipeline)

    # Afficher les résultats
    for resultat in resultats:
        # Supprimer "Back to top" du résultat
        genre = resultat["_id"]
        # Ajouter un espace avant chaque majuscule
        genre = ''.join([' ' + i if i.isupper() else i for i in genre]).strip()
        # Afficher la durée moyenne arrondie
        duree_arrondie = round(resultat["duree_moyenne"])
        st.write(genre, ": durée moyenne =", duree_arrondie,"minutes")

elif onglet == "recherche":
    
        def search_movies(title=None, actors=None, genre=None, max_duration=None, min_score=None):
            # Créer un dictionnaire avec les critères de recherche
            query = {}
            if title:
                query["titre"] = {"$regex": title, "$options": "i"}  # Recherche insensible à la casse
            if actors:
                query["acteurs"] = {"$all": actors}  # Recherche tous les acteurs donnés
            if genre:
                query["genre"] = genre
            if max_duration:
                query["duree"] = {"$lte": max_duration}  # Recherche des films dont la durée est inférieure ou égale à max_duration
            if min_score:
                query["score"] = {"$gte": min_score}  # Recherche des films dont la note est supérieure ou égale à min_score

            # Effectuer la recherche
            resultats = collection.find(query)

            # Afficher les résultats
            st.write("Résultats de la recherche :")
            for resultat in resultats:
                st.write("- Titre :", resultat["titre"])
                st.write("  Année :", resultat["annee"])
                st.write("  Genre :", resultat["genre"])
                st.write("  Acteurs :", ''.join(resultat["acteurs"]))
                st.write("  Durée :", resultat["duree"], "minutes")
                st.write("  Score :", resultat["score"])


        # Interface utilisateur Streamlit
        st.title("Recherche de films")

        # Recherche par titre
        st.subheader("Recherche par titre")
        titre = st.text_input("Titre du film")
        if st.button("Rechercher"):
            search_movies(title=titre)

        # # Recherche par acteurs
        # st.subheader("Recherche par acteurs")
        # acteurs = st.text_input("Acteurs (séparés par des virgules)")
        # if st.button("Rechercher"):
        #     search_movies(actors=acteurs.split(','))

        # # Recherche par genre
        # st.subheader("Recherche par genre")
        # genres = ["Action", "Aventure", "Comédie", "Drame", "Horreur", "Science-fiction"]
        # genre = st.selectbox("Genre", genres)
        # if st.button("Rechercher"):
        #     search_movies(genre=genre)

        # # Recherche par durée
        # st.subheader("Recherche par durée")
        # duree = st.number_input("Durée maximale (en minutes)", min_value=0, max_value=300, step=10)
        # if st.button("Rechercher"):
        #     search_movies(max_duration=duree)

        # # Recherche par note
        # st.subheader("Recherche par note")
        # note = st.slider("Note minimale", min_value=0, max_value=10, step=0.5)
        # if st.button("Rechercher"):
        #     search_movies(min_score=note)