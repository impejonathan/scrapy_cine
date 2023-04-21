import streamlit as st
from pymongo import MongoClient
import pymongo
import pandas as pd
from dotenv import load_dotenv
import os
from stream_recherche import *
from streal_question import *

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer la clé d'API Atlas à partir des variables d'environnement
ATLAS_KEY = os.getenv('ATLAS_KEY')

# Se connecter à la base de données IMDb dans Atlas
client = MongoClient(ATLAS_KEY)
db = client["imdb"]
collection = db["top_imdb"]


# Sidebar pour sélectionner l'onglet
onglet = st.sidebar.selectbox("Choisissez un onglet", ["question", "recherche"])


if onglet == "question":

    question()


elif onglet == "recherche":
    
        titre = st.text_input("Titre du film")
        
        # Créer un bouton pour lancer la recherche
        if st.button("Rechercher"):
            # Appeler la fonction search_movies() avec le titre du film en tant qu'argument
            search_movies(collection, title=titre)



        # Connexion à la base de données
        db = client["bdd"]
        collection = db["top_imdb"]

        def afficher_resultats(acteur_selectionne):
            """
            Fonction pour afficher les résultats de la recherche avec l'acteur sélectionné
            """
            # Recherche des films avec l'acteur sélectionné
            resultats = collection.find({"acteurs": {"$in": [acteur_selectionne]}})

            # Concaténation des résultats en une seule ligne
            resultat_str = ""
            for resultat in resultats:
                resultat_str += f"{resultat['titre']} -- ({resultat['annee']}) --{resultat['duree']} min | " 

            # Affichage des résultats
            st.write("Résultats de la recherche :", resultat_str[:-3])

        # Formulaire de recherche
        st.write("# Recherche de films par acteur")

        # Récupération de la liste des acteurs
        acteurs = collection.distinct("acteurs")

        # Sélection de l'acteur
        acteur_selectionne = st.selectbox("Sélectionnez un acteur", acteurs)

        # Affichage des résultats
        afficher_resultats(acteur_selectionne)

        recherche_films_par_duree(collection)
        

        # Interface utilisateur
        st.title("Recherche de films par note")

        # Récupérer toutes les notes disponibles dans la base de données
        notes = collection.distinct("score")

        # Créer un menu déroulant pour sélectionner la note
        selected_score = st.selectbox("Sélectionner une note", notes, key='score_selectbox')

        # Bouton pour effectuer la recherche
        if st.button("Rechercher par note", key="rechercher_par_note"):
            search_by_score(collection, selected_score)
                    
            
            # /////////////////////////////////////////////
            
        # Récupération de la liste des genres
        genres = collection.distinct("genre")

        # Sélection du genre
        genre_selectionne = st.selectbox("Sélectionnez un genre", genres)

        # Recherche des films avec le genre sélectionné
        resultats = collection.find({"genre": genre_selectionne})

        # Affichage des résultats
        st.write("Résultats de la recherche :")
        for resultat in resultats:
            st.text("- Titre : "+ resultat["titre"] +"   Durée du film : "+ str(resultat["duree"])+ "minutes" + "  Score du film : "+ resultat["score"])
       
