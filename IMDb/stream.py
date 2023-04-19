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
db = client["imdb"]
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
    # Calculer la durée moyenne d'un film en fonction de son genre
    pipeline = [
        {"$group": {"_id": "$genre", "duree_moyenne": {"$avg": "$duree"}}},
        {"$sort": {"_id": 1}}
    ]
    resultats = collection.aggregate(pipeline)

    # Afficher les résultats
    for resultat in resultats:
        # Supprimer "Back to top" du résultat
        genre = resultat["_id"].replace("Back to top", "")
        # Ajouter un espace avant chaque majuscule
        genre = ''.join([' ' + i if i.isupper() else i for i in genre]).strip()
        # Afficher la durée moyenne arrondie
        duree_arrondie = round(resultat["duree_moyenne"])
        st.write(genre, ": durée moyenne =", duree_arrondie,"minutes")

elif onglet == "recherche":
    
        def search_movies(title=None, actors=None, genre=None, max_duration=None, min_score=None):
            """
                Recherche des films dans une collection MongoDB en utilisant différents critères de recherche.

                Args:
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



        # Interface utilisateur Streamlit
        st.title("Recherche de films")

        # Recherche par titre
        st.subheader("Recherche par titre")
        titre = st.text_input("Titre du film")
        if st.button("Rechercher"):
            search_movies(title=titre)
            
        

        # Définir la fonction de recherche par acteur(s)
        def search_by_actor():
            """
                Recherche des films dans une collection MongoDB en utilisant le nom d'un ou plusieurs acteurs.

                Args:
                    None.

                Returns:
                    None. La fonction affiche les résultats de la recherche dans la console.
            """
            # Entrée de l'utilisateur pour les acteurs
            actors_input = st.text_input("Entrez le nom d'acteur(s) séparé(s) par des virgules (ex: Tom Cruise, Brad Pitt)")

            # Vérification de l'entrée de l'utilisateur
            if not actors_input:
                st.warning("Veuillez entrer le nom d'acteur(s)")
                return

            actors = [a.strip() for a in actors_input.split(",")]

            # Requête à la base de données
            query = {"acteurs": {"$all": actors}}
            resultats = collection.find(query)

            # Affichage des résultats
            st.write("Résultats de la recherche :")
            for resultat in resultats:
                # Supprimer "Back to top" du genre
                genre = resultat["genre"].replace("Back to top", "")
                # Ajouter un espace avant chaque majuscule dans le genre
                genre = ''.join([' ' + i if i.isupper() else i for i in genre]).strip()
                # Ajouter un espace avant chaque majuscule dans les noms d'acteur
                acteurs = [a.title() for a in resultat["acteurs"]]
                st.write("- Titre :", resultat["titre"])
                st.write("  Année :", resultat["annee"])
                st.write("  Genre :", genre)
                st.write("  Acteurs :", ', '.join(acteurs))
                st.write("  Durée :", resultat["duree"], "minutes")
                st.write("  Score :", resultat["score"])

        # # Application Streamlit
        # st.title("Recherche de films")
        # option = st.sidebar.selectbox("Choisissez une option", ["Recherche par acteur(s)"])

        # # Affichage de la recherche par acteur(s)
        # if option == "Recherche par acteur(s)":
        #     search_by_actor()


        db = client["bdd"]
        collection = db["top_imdb"]


        # Formulaire de recherche
        st.write("# Recherche de films par acteur")

        # Récupération de la liste des acteurs
        acteurs = collection.distinct("acteurs")

        # Sélection de l'acteur
        acteur_selectionne = st.selectbox("Sélectionnez un acteur", acteurs)

        # Recherche des films avec l'acteur sélectionné
        resultats = collection.find({"acteurs": {"$in": [acteur_selectionne]}})

        # Affichage des résultats
        st.write("Résultats de la recherche :")
        for resultat in resultats:
            st.write("- Titre :", resultat["titre"])
            st.write("  Année :", resultat["annee"])
            st.write("  Genre :", resultat["genre"])
            st.write("  Acteurs :", resultat["acteurs"])
            st.write("  Durée :", resultat["duree"], "minutes")
            st.write("  Score :", resultat["score"])
            
            
            
            
            
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
                # Supprimer "Back to top" du genre
                # Ajouter un espace avant chaque majuscule
                # genre = ''.join([' ' + i if i.isupper() else i for i in genre]).strip()
                st.write("- Titre :", resultat["titre"])
                st.write("  Année :", resultat["annee"])
                # st.write("  Genre :", genre)
                st.write("  Acteurs :", ', '.join(resultat["acteurs"]))
                st.write("  Durée :", resultat["duree"], "minutes")
                st.write("  Score :", resultat["score"])

        # Interface utilisateur
        st.title("Recherche de films par durée")
        max_duration = st.slider("Durée maximale de film (en minutes)", 0, 300, 120)
        if st.button("Rechercher par durée", key="rechercher_duree"):
            search_by_duration(max_duration)
            
            
        

        def search_by_score(score):
            """
            Recherche les titres de films ayant une note donnée.
            
            :param score: la note à rechercher
            """
            # Convertir la note sélectionnée en float
            score = str(score)
            
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

        # Interface utilisateur
        st.title("Recherche de films par note")

        # Récupérer toutes les notes disponibles dans la base de données
        notes = collection.distinct("score")

        # Créer un menu déroulant pour sélectionner la note
        selected_score = st.selectbox("Sélectionner une note", notes)

        # Bouton pour effectuer la recherche
        if st.button("Rechercher par note", key="rechercher_par_note"):
            search_by_score(selected_score)

