import os

dossier_racine = "C:/Users/leogu/Desktop/SAE/output"

# Parcourt les sous-dossiers du dossier racine
for sous_dossier in os.listdir(dossier_racine):
    sous_dossier_path = os.path.join(dossier_racine, sous_dossier)

    if os.path.isdir(sous_dossier_path):  # Vérifie si le chemin est un dossier
        # Parcourt les fichiers dans chaque sous-dossier
        for fichier in os.listdir(sous_dossier_path):
            if fichier.endswith('.json'):
                nouveau_nom = sous_dossier + '.json'
                fichier_path = os.path.join(sous_dossier_path, fichier)
                nouveau_path = os.path.join(sous_dossier_path, nouveau_nom)

                # Renomme le fichier avec le nouveau nom
                os.rename(fichier_path, nouveau_path)
                print(f'Fichier renommé : {fichier} -> {nouveau_nom}')

        # Renomme le fichier JSON dans le sous-dossier racine
        fichier_json = os.path.join(sous_dossier_path, sous_dossier + '.json')
        os.rename(fichier_json, os.path.join(dossier_racine, sous_dossier + '.json'))

        # Supprime le sous-dossier maintenant vide
        os.rmdir(sous_dossier_path)

print('Opération terminée.')
