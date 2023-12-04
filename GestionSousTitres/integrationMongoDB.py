import os
import pymongo
import json
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

# Connexion à MongoDB
print("Connexion à MongoDB...")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sae"]
collection = db["series"]

# Chemin des fichiers JSON de sous-titres
dossier_sous_titres = "C:/Users/leogu/Desktop/SAE/output"

# Parcours des fichiers du dossier
for fichier in os.listdir(dossier_sous_titres):
    if fichier.endswith(".json"):
        chemin_fichier = os.path.join(dossier_sous_titres, fichier)

        # Import du fichier JSON dans MongoDB
        print(f"Import du fichier {chemin_fichier} dans MongoDB...")
        with open(chemin_fichier, "r", encoding="utf-8") as file:
            subtitles_data = json.load(file)
            series_title = None
            text = None
            for subtitle in subtitles_data:
                if "series_title" in subtitle:
                    series_title = subtitle["series_title"]
                elif "text" in subtitle:
                    text = subtitle["text"]
                if series_title and text:
                    collection.insert_one({"series_title": series_title, "text": text})
                    print(f"Document inséré dans la collection avec le titre de série : {series_title}")
                    series_title = None
                    text = None

# Connexion au serveur MongoDB source et sélection de la base de données et de la collection source
print("Connexion au serveur MongoDB source...")
client_src = MongoClient('mongodb://localhost:27017')
db_src = client_src['sae']
collection_src = db_src['series']

# Connexion au serveur MongoDB de destination et sélection de la base de données et de la collection de destination
print("Connexion au serveur MongoDB de destination...")
client_dest = MongoClient('mongodb://localhost:27017')
db_dest = client_dest['application_sae']
collection_dest = db_dest['series']

# Création d'un objet TfidfVectorizer
print("Création de l'objet TfidfVectorizer...")
tfidf_vectorizer = TfidfVectorizer()

# Ajout du texte à la liste
texts = [document['text'] for document in collection_src.find()]

# Calcul des valeurs de TF-IDF pour chaque mot dans les textes
print("Calcul des valeurs de TF-IDF...")
tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

# Liste des mots (features) dans l'ordre
feature_names = tfidf_vectorizer.get_feature_names_out()

# Parcours des documents dans la collection source
print("Parcours des documents dans la collection source...")
for idx, document in enumerate(collection_src.find()):
    series_title = document['series_title']
    text = document['text']

    # Création d'un dictionnaire pour stocker les poids des mots
    word_weights = {}

    # Récupération des valeurs de TF-IDF pour le document actuel
    feature_index = tfidf_matrix[idx, :].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[idx, x] for x in feature_index])

    # Stockage des poids des mots dans le dictionnaire
    for word_index, score in [(feature_names[i], s) for (i, s) in tfidf_scores]:
        word_weights[word_index] = score

    # Création d'un nouveau document pour la collection de destination
    new_document = {
        'titre_serie': series_title,
        'mots': word_weights
    }

    # Insertion du nouveau document dans la collection de destination
    collection_dest.insert_one(new_document)
    print(f"Document inséré dans la collection de destination avec le titre de série : {series_title}")

# Suppression de la base de données source
print("Suppression de la base de données source...")
client_src.drop_database('sae')

# Fermeture des connexions aux serveurs MongoDB
print("Fermeture des connexions aux serveurs MongoDB...")
client_src.close()
client_dest.close()
client.close()
print("Programme terminé.")
