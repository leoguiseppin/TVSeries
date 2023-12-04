# Importation des modules nécessaires
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from translate import Translator
from flask_login import current_user, LoginManager, UserMixin, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt
from collections import Counter
from urllib.parse import urlencode
from random import sample

# Création de l'application Flask
app = Flask(__name__)
app.secret_key = 'clef_secrete_sae'  # Clé secrète pour la sécurité des sessions

# Initialisation de Bcrypt pour le hachage de mots de passe
bcrypt = Bcrypt(app)

# Configuration du gestionnaire de connexion
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirection vers la page de connexion en cas de besoin

# Configuration de la connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['application_sae']
collection_series = db['series']
collection_utilisateurs = db['utilisateurs']

# Classe pour représenter un utilisateur
class Utilisateur(UserMixin):
    def __init__(self, identifiant):
        self.identifiant = identifiant
        self.series_aimees = []

    def get_id(self):
        return self.identifiant


# Fonction pour charger un utilisateur depuis la base de données
@login_manager.user_loader
def load_user(identifiant):
    utilisateur = collection_utilisateurs.find_one({'identifiant': identifiant})
    
    if utilisateur:
        user = Utilisateur(utilisateur['identifiant'])
        return user

    return None


# Page de connexion
@app.route('/', methods=['GET', 'POST'])
def login():
    message = request.args.get('message', '')
    message_type = request.args.get('message_type', '')

    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = collection_utilisateurs.find_one({'identifiant': identifiant})

        if utilisateur and bcrypt.check_password_hash(utilisateur['mot_de_passe'], mot_de_passe):
            user = Utilisateur(identifiant)
            login_user(user)
            message = "Connexion réussie."
            message_type = "success"
            return redirect(url_for('search_series', message=message, message_type=message_type))
        else:
            message = "Identifiants invalides. Réessayez."
            message_type = "error"

    return render_template('login.html', message=message, message_type=message_type)


# Page de déconnexion
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user
    message = "Déconnexion réussie."
    message_type = 'success'
    return redirect(url_for('login', message=message, message_type=message_type))


# Page d'inscription
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    message = ''
    message_type = ''

    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mot_de_passe = request.form['mot_de_passe']
        hashed_password = bcrypt.generate_password_hash(mot_de_passe).decode('UTF-8')

        if collection_utilisateurs.find_one({'identifiant': identifiant}):
            message = "Cet identifiant est déjà utilisé."
            message_type = "error"
        else:
            collection_utilisateurs.insert_one({'identifiant': identifiant, 'mot_de_passe': hashed_password, 'series_aimees': []})
            return redirect(url_for('login', message="Inscription réussie. Vous pouvez maintenant vous connecter.", message_type="success"))

    return render_template('inscription.html', message=message, message_type=message_type)


# Fonction pour obtenir des titres de séries aléatoires
def get_random_series_titles(count=21):
    series_list = list(collection_series.find({}, {'titre_serie': 1, '_id': 0}))
    random_series_titles = [series['titre_serie'] for series in sample(series_list, count)]
    return random_series_titles


# Page de recherche de séries
@app.route('/recherche', methods=['GET', 'POST'])
@login_required
def search_series():
    top_series = []
    utilisateur = collection_utilisateurs.find_one({'identifiant': current_user.identifiant})
    
    if utilisateur:
        series_aimees = set(utilisateur.get('series_aimees', []))
    else:
        series_aimees = set()

    if request.method == 'POST':
        search_query = request.form['search_query']
        search_words = search_query.split()
        series_occurrences = {}
        translated_words = []
        translator = Translator(to_lang="en")

        for word in search_words:
            translated_word = translator.translate(word)
            translated_words.extend([word, translated_word])

        for document in collection_series.find():
            titre_serie = document['titre_serie']
            mots = document['mots']
            total_occurrences = 0

            for word in translated_words:
                total_occurrences += mots.get(word, 0)

            if total_occurrences > 0:
                series_occurrences[titre_serie] = total_occurrences

        if not series_occurrences:
            random_series_titles = get_random_series_titles()
            top_series = [(titre_serie, 0) for titre_serie in random_series_titles]
        else:
            sorted_series = sorted(series_occurrences.items(), key=lambda x: x[1], reverse=True)
            top_series = sorted_series[:21]

    else:
        random_series_titles = get_random_series_titles()
        top_series = [(titre_serie, 0) for titre_serie in random_series_titles]

    return render_template('recherche.html', top_series=top_series, series_aimees=series_aimees)


# Endpoint pour like ou dislike une série
@app.route('/like_series/<titre_serie>', methods=['POST'])
@login_required
def like_series(titre_serie):
    utilisateur = collection_utilisateurs.find_one({'identifiant': current_user.identifiant})

    if utilisateur:
        series_aimees = utilisateur.get('series_aimees', [])
        if titre_serie in series_aimees:
            series_aimees.remove(titre_serie)
            response = "unliked"
        else:
            series_aimees.append(titre_serie)
            response = "liked"

        collection_utilisateurs.update_one({'_id': utilisateur['_id']}, {'$set': {'series_aimees': series_aimees}})
    
    return jsonify(response)


# Page de recommandations de séries
@app.route('/recommandations')
@login_required
def recommandations():
    top_series = []
    utilisateur = collection_utilisateurs.find_one({'identifiant': current_user.identifiant})
    series_aimees = set(utilisateur.get('series_aimees', []))

    if not series_aimees:
        random_series_titles = get_random_series_titles()
        top_series = [(titre_serie, 0) for titre_serie in random_series_titles]
    else:
        mots_cles_frequents = []

        for titre_serie in series_aimees:
            series = collection_series.find_one({'titre_serie': titre_serie})
            if series:
                mots = series.get('mots', {})
                top_mots = sorted(mots.items(), key=lambda item: item[1], reverse=True)[:5]
                mots_cles_frequents.extend([mot[0] for mot in top_mots])
        
        series_occurrences = {}

        for document in collection_series.find():
            titre_serie = document['titre_serie']

            if titre_serie in series_aimees:
                continue

            mots = document['mots']
            total_occurrences = 0

            for word in mots_cles_frequents:
                total_occurrences += mots.get(word, 0)

            series_occurrences[titre_serie] = total_occurrences

        sorted_series = sorted(series_occurrences.items(), key=lambda x: x[1], reverse=True)
        top_series = sorted_series[:21]

    return render_template('recommandations.html', top_series=top_series, series_aimees=series_aimees)


# Page du profil de l'utilisateur
@app.route('/profil')
@login_required
def profil():
    utilisateur = collection_utilisateurs.find_one({'identifiant': current_user.identifiant})
    
    if utilisateur:
        series_aimees = utilisateur.get('series_aimees', [])
    else:
        series_aimees = []

    return render_template('profil.html', series_aimees=series_aimees)


# Page de suppression du compte utilisateur
@app.route('/suppression', methods=['GET', 'POST'])
@login_required
def suppression():
    if request.method == 'POST':
        confirmation = request.form.get('confirmation')

        if confirmation.lower() == "supprimer":
            collection_utilisateurs.delete_one({'identifiant': current_user.identifiant})
            logout_user()
            message = "Votre compte a été supprimé avec succès."
            message_type = "success"
            return render_template('login.html', message=message, message_type=message_type)
        else:
            message = "La confirmation est incorrecte. Réessayez."
            message_type = "error"
            return render_template('suppression.html', message=message, message_type=message_type)

    return render_template('suppression.html')


# Point d'entrée de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
