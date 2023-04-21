import streamlit as st
from pymongo import MongoClient
import pymongo
import pandas as pd
from dotenv import load_dotenv
import os
from pymongo.collection import Collection


# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé d'API Atlas à partir des variables d'environnement
ATLAS_KEY = os.getenv('ATLAS_KEY')

# Se connecter à la base de données IMDb dans Atlas
client = MongoClient(ATLAS_KEY)
db = client["imdb"]
collection = db["top_imdb"]



def search_movies(collection, title=None, actors=None, genre=None, max_duration=None, min_score=None):
    """
        Recherche des films dans une collection MongoDB en utilisant différents critères de recherche.

        Args:
            collection (pymongo.collection.Collection): Collection MongoDB contenant les données des films.
            title (str, optional): Titre du film à rechercher. Recherche insensible à la casse.
            actors (list, optional): Liste des acteurs du film à rechercher. Recherche tous les acteurs donnés.
            genre (str, optional): Genre du film à rechercher.
            max_duration (int, optional): Durée maximale du film en minutes.
            min_score (float, optional): Note minimale du film.

        Returns:
            None. La fonction affiche les résultats de la recherche dans la console.
    """
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
        # Supprimer "Back to top" du genre
        genre = resultat["genre"].replace("Back to top", "")
        # Ajouter un espace avant chaque majuscule dans le genre
        genre = ''.join([' ' + i if i.isupper() else i for i in genre]).strip()
        # Ajouter un espace avant chaque majuscule dans le nom des acteurs
        acteurs = ''.join([' ' + i if i.isupper() else i for i in resultat["acteurs"]]).strip()
        st.write("- Titre :", resultat["titre"])
        st.write("  Année :", resultat["annee"])
        st.write("  Genre :", genre)
        st.write("  Acteurs :", acteurs)
        st.write("  Durée :", resultat["duree"], "minutes")
        st.write("  Score :", resultat["score"])
        
        
        
        
# ////////////////////////////////////////////////////////////////

client = MongoClient(ATLAS_KEY)
db = client["imdb"]
collection = db["top_imdb"]

def recherche_films_par_duree(collection):
    # Fonction de recherche par durée
    def search_by_duration(max_duration):
        """
        Recherche des films dont la durée est inférieure ou égale à max_duration.
            
        Args:
        max_duration (int): La durée maximale du film en minutes.

        Returns:
        None. Affiche les résultats de la recherche dans l'interface utilisateur.
        """
            
        # Créer un dictionnaire de recherche
        query = {"duree": {"$lte": max_duration}}

        # Effectuer la recherche
        resultats = collection.find(query)

        # Afficher les résultats
        st.write("Résultats de la recherche :")
        for resultat in resultats:
            st.write("- Titre :", resultat["titre"])
            st.write("  Année :", resultat["annee"])
            st.write("  Genre :", resultat["genre"])
            st.write("  Acteurs :", ', '.join(resultat["acteurs"]))
            st.write("  Durée :", resultat["duree"], "minutes")
            st.write("  Score :", resultat["score"])

    # Interface utilisateur
    st.title("Recherche de films par durée")
    max_duration = st.slider("Durée maximale de film (en minutes)", 0, 300, 120)
    if st.button("Rechercher par durée", key="rechercher_duree"):
        search_by_duration(max_duration)
        
def search_by_score(collection: Collection, score: str):
    """
    Recherche les titres de films ayant une note donnée.
    
    :param collection: La collection de la base de données MongoDB
    :param score: la note à rechercher
    """
    # Créer un dictionnaire de recherche
    query = {"score": score}

    # Effectuer la recherche
    resultats = collection.find(query)

    # Afficher les titres des films correspondants
    i = 0
    for resultat in resultats:
        i += 1
        st.write(f"{i}. Titre : {resultat['titre']}")

    # Afficher un message si aucun résultat n'est trouvé
    if i == 0:
        st.write("Aucun résultat trouvé pour cette note.")