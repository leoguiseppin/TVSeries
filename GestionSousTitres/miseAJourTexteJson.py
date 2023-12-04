import os
import json
import re

# Définir la fonction pour supprimer les chiffres et nombres d'une chaîne de caractères
def remove_numbers(text):
    return re.sub(r'\d+', '', text)

# Chemin d'accès au dossier racine contenant les fichiers JSON
dossier_racine = "C:/Users/leogu/Desktop/SAE/output"

# Parcourir tous les fichiers du dossier racine
for nom_fichier in os.listdir(dossier_racine):
    if nom_fichier.endswith(".json"):
        chemin_fichier = os.path.join(dossier_racine, nom_fichier)
        
        # Charger le fichier JSON
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier_json:
            data = json.load(fichier_json)

        # Utiliser une liste de compréhension pour extraire les champs "text"
        texts = [element["text"] if "text" in element else "" for element in data]

        # Appliquer la fonction remove_numbers à chaque élément de la liste "texts"
        texts = [remove_numbers(text) for text in texts]

        # Rassembler les textes en une seule chaîne
        text_combined = ' '.join(texts)

        # Mettre à jour le champ "text" dans le JSON d'origine avec la valeur de "text_combined"
        for element in data:
            if "text" in element:
                element["text"] = text_combined

        # Supprimer tous les éléments "text" sauf le premier
        text_elements_to_remove = [element for element in data if "text" in element][1:]
        for element in text_elements_to_remove:
            data.remove(element)

        # Réécrire le fichier JSON d'origine avec les modifications
        with open(chemin_fichier, 'w', encoding='utf-8') as fichier_json:
            json.dump(data, fichier_json, indent=4)

        print(f"Champ 'text' mis à jour avec succès dans 'text_combined' dans le fichier {nom_fichier}.")
