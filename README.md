# Projet : Récupérer des données et créer votre application

Ce projet consiste à récupérer des données de films et séries sur IMDb, à les stocker dans une base de données MongoDB et à créer une application avec Streamlit pour afficher les résultats.

### Partie 1 : analyser le html pour le Scrapper

    Regardez la série de vidéos suggérée pour apprendre à utiliser Scrapy pour extraire les données de la page web.
    Si vous n'êtes pas familier avec les sélecteurs CSS et XPATH, faites quelques recherches à ce sujet.

### Partie 2 : Scraper IMDb

Récupérez les données de :

    Top 250 des meilleurs films
    Top 250 des meilleures séries
    [Facultatif] Tous les films
    [Facultatif] Uniquement certains genres de film (action, horreur, etc.)

Extraire les informations suivantes :

    Titre
    Titre original
    Score
    Genre
    Année
    Durée (en minutes)
    Description (synopsis)
    Acteurs (Casting principal)
    Public
    Pays
    [facultatif] Langue d’origine
    [facultatif] Informations spécifiques aux séries : Nombre de saisons, Nombre d’épisodes

### Partie 3 : le Streamlit

Ce code utilise le module Streamlit pour afficher des résultats à partir d'une base de données MongoDB contenant des informations sur les films.
Prérequis

    Python 3
    Streamlit
    pymongo
    pandas
    dotenv

Configuration

Le fichier .env contient la clé d'API Atlas nécessaire pour se connecter à la base de données.
Utilisation

Exécutez le fichier main.py pour lancer l'application Streamlit. L'application comporte deux onglets : "question" et "recherche".
Onglet "question"

Cet onglet répond à plusieurs questions sur les films contenus dans la base de données. Voici les questions et les réponses correspondantes :

    Q1 : Quel est le film le plus long ?
    Q2 : Quels sont les 5 films les mieux notés ?
    Q3 : Dans combien de films a joué Morgan Freeman ? Tom Cruise ?
    Q4 : Quels sont les 3 meilleurs films d’horreur ? Dramatique ? Comique ?
    Q5 : Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?
    Q6 : Quelle est la durée moyenne d'un film en fonction du genre ?

Onglet "recherche"

Cet onglet permet à l'utilisateur de rechercher des films dans la base de données en fonction de différents critères, tels que le titre, le genre, l'année de sortie, etc. Les résultats de la recherche sont affichés dans un tableau.
