import os
import json
import re

# Liste de mots vides en français et en anglais
mots_vides = set([
    "a", "about", "above", "after", "again", "against", "ain't", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "couldn't", "d", "did", "didn't",
    "do", "does", "doesn't", "doing", "don", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "her", "here", "hers", "herself", "him", "himself",
    "his", "how", "i", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
    "just", "ll", "m", "ma", "me", "mightn't", "more", "most", "mustn't", "my",
    "myself", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same",
    "shan't", "she", "she's", "should", "should've", "shouldn't", "so", "some",
    "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then",
    "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "ve", "very", "was", "wasn't", "we", "were", "weren't", "what", "when",
    "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn't", 
    "y", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",
    "a", "abord", "afin", "ah", "ai", "aie", "aient", "aies", "ailleurs", "ainsi", "allaient", "allo", "allons",
    "allô", "alors", "anterieur", "anterieure", "anterieures", "apres", "après", "as", "assez", "attendu",
    "au", "aucun", "aucune", "aujourd", "aujourd'hui", "aupres", "auquel", "aura", "aurai", "auraient",
    "aurais", "aurait", "auras", "aurez", "auriez", "aurions", "aurons", "auront", "aussi", "autre",
    "autres", "autrui", "aux", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec",
    "avez", "aviez", "avions", "avons", "ayant", "ayante", "ayantes", "ayants", "ayez", "ayons", "b", "bah",
    "bas", "basee", "bat", "beau", "beaucoup", "bien", "bigre", "boum", "bravo", "brrr", "c", "car", "ce",
    "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci",
    "celui-là", "celà", "cent", "cependant", "certain", "certaine", "certaines", "certains", "certes",
    "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "chacun", "chacune", "chaque", "cher", "chers",
    "chez", "chiche", "chut", "chère", "chères", "ci", "cinq", "cinquantaine", "cinquante", "cinquantième",
    "cinquième", "clac", "clic", "combien", "comme", "comment", "comparable", "comparables", "compris",
    "concernant", "contre", "couic", "crac", "d", "da", "dans", "de", "debout", "dedans", "dehors", "deja",
    "delà", "depuis", "dernier", "derniere", "derriere", "derrière", "des", "desormais", "desquelles",
    "desquels", "dessous", "dessus", "deux", "deuxième", "deuxièmement", "devant", "devers", "devra", "different",
    "differentes", "differents", "différent", "différente", "différentes", "différents", "dire", "directe",
    "directement", "dit", "dite", "dits", "divers", "diverse", "diverses", "dix", "dix-huit", "dix-neuf",
    "dix-sept", "dixième", "doit", "doivent", "donc", "dont", "dos", "douze", "douzième", "dring", "du", "duquel",
    "durant", "dès", "début", "désormais", "e", "effet", "egale", "egalement", "egales", "eh", "elle", "elle-même",
    "elles", "elles-mêmes", "en", "encore", "enfin", "entre", "envers", "environ", "es", "essai", "est", "et", "eu",
    "eue", "eues", "euh", "eurent", "eus", "eusse", "eussent", "eusses", "eussiez", "eussions", "eut", "eux", "eûmes",
    "eût", "eûtes", "f", "fais", "faisaient", "faisant", "fait", "façon", "feront", "fi", "flac", "floc", "font",
    "g", "gens", "h", "ha", "haut", "hein", "hem", "hep", "hi", "ho", "holà", "hop", "hormis", "hors", "hou", "houp",
    "hue", "hui", "huit", "huitième", "hum", "hurrah", "hé", "hélas", "i", "ici", "il", "ils", "j", "je", "jusqu",
    "jusque", "juste", "k", "l", "la", "laisser", "laquelle", "las", "le", "lequel", "les", "lesquelles", "lesquels",
    "leur", "leurs", "longtemps", "lors", "lorsque", "lui", "lui-meme", "lui-même", "là", "lès", "m", "ma", "maint",
    "maintenant", "mais", "malgre", "malgré", "maximale", "me", "meme", "memes", "merci", "mes", "mien", "mienne",
    "miennes", "miens", "mille", "mince", "minimale", "moi", "moi-meme", "moi-même", "moindres", "moins", "mon",
    "moyennant", "même", "mêmes", "n", "na", "ne", "neanmoins", "necessaire", "necessairement", "neuf", "neuvième",
    "ni", "nombreuses", "nombreux", "nommés", "non", "nos", "notre", "nous", "nous-mêmes", "nouveau", "nouveaux",
    "nul", "néanmoins", "nôtre", "nôtres", "o", "oh", "ohé", "ollé", "olé", "on", "ont", "onze", "onzième", "ore",
    "ou", "ouf", "ouias", "oust", "ouste", "outre", "ouvert", "ouverte", "ouverts", "o|", "où", "p", "par", "parce",
    "parfois", "parle", "parlent", "parler", "parmi", "parole", "parseme", "partant", "particulier", "particulière",
    "particulièrement", "pas", "passé", "pendant", "pense", "permet", "personne", "personnes", "peu", "peut", "peuvent",
    "peux", "pff", "pfft", "pfut", "pif", "pire", "pièce", "plein", "plouf", "plupart", "plus", "plusieurs", "plutôt",
    "possessif", "possessifs", "possible", "possibles", "pouah", "pour", "pourquoi", "pourrais", "pourrait", "pouvait",
    "prealable", "precisement", "premier", "première", "premièrement", "pres", "probable", "probante", "procedant",
    "proche", "près", "psitt", "pu", "puis", "puisque", "pur", "pure", "q", "qu", "quand", "quant", "quanta", "quant-à-soi",
    "quarante", "quatorze", "quatre", "quatre-vingt", "quatrième", "quatrièmement", "que", "quel", "quelconque", "quelle",
    "quelles", "quelqu'un", "quelque", "quelques", "quels", "qui", "quiconque", "quinze", "quoi", "quoique", "r", "rare",
    "rarement", "rares", "relative", "relativement", "remarquable", "rend", "rendre", "restant", "reste", "restent", "restrictif",
    "retour", "revoici", "revoilà", "rien", "s", "sa", "sacrebleu", "sait", "sans", "sapristi", "sauf", "se", "sein", "seize", "selon",
    "semblable", "semblaient", "semble", "semblent", "sent", "sept", "septième", "sera", "serai", "seraient", "serais", "serait", "seras",
    "serez", "seriez", "serions", "serons", "seront", "ses", "seul", "seule", "seulement", "si", "sien", "sienne", "siennes", "siens", "sinon",
    "six", "sixième", "soi", "soi-même", "soit", "soixante", "son", "sont", "sous", "souvent", "soyez", "soyons", "suis", "suite", "suivant",
    "suivante", "suivantes", "suivants", "suivre", "sur", "surtout", "t", "ta", "tac", "tandis", "tant", "tardive", "te", "tel", "telle", "tellement",
    "telles", "tels", "tenant", "tend", "tenir", "tente", "tes", "tic", "tien", "tienne", "tiennes", "tiens", "toc", "toi", "toi-même", "ton",
    "touchant", "toujours", "tous", "tout", "toute", "toutefois", "toutes", "treize", "trente", "tres", "trois", "troisième", "troisièmement", "trop",
    "très", "tsoin", "tsouin", "tu", "té", "u", "un", "une", "unes", "uniformement", "unique", "uniques", "uns", "v", "va", "vais", "vas", "vers",
    "via", "vif", "vifs", "vingt", "vivat", "vive", "vives", "vlan", "voici", "voie", "voient", "voilà", "vont", "vos", "votre", "vous", "vous-mêmes",
    "vu", "vé", "vôtre", "vôtres", "w", "x", "y", "z", "zut", "à", "â", "ça", "ès", "étaient", "étais", "était", "étant", "été", "être", "ô", "know",
    "could", "want", "tell", "ca", "think", "look", "really", "something", "gonna", "back", "need", "good", "yes", "mean", "us", "would", "take",
    "way", "uh", "dois", "hey", "little", "bon", "mr", "even", "sorry", "man", "cause", "talk", "years", "fois", "sorry", "new", "wait", "maybe",
    "still", "told", "accord", "fois", "found", "ü", "fuck", "accord", "besoin", "make", "sure", "found", "help", "day", "talk", "fucking", "need",
    "salut", "hello", "time", "thing", "life", "old", "away", "chose", "cest", "im", "jai", "sais", "yeah", "well", "veux", "faire", "oui", "okay",
    "youre", "right", "like", "go", "get", "ok", "vraiment", "quil", "thats", "going", "quon", "nest", "got", "ouais", "aller", "voir", "see",
    "one", "didnt", "cétait", "never", "jamais", "come", "said", "peutêtre", "cant", "guy", "hes", "ans", "questce", "say", "quelquun", "ill",
    "wasnt", "sest", "two", "thought", "let", "went", "êtes", "saw", "lai", "ever", "whats", "minutes", "faut", "sir", "temps", "find", "people",
    "theres", "thank", "please", "dr", "trouvé", "savez", "dun", "avoir", "anything", "work", "ive", "believe", "theyre", "happened", "door", "may",
    "last", "shes", "looking", "sil", "unsub", "first", "veut", "daccord", "doesnt", "type", "someone", "much", "youve", "crois", "nai", "id",
    "mec", "tas", "yo", "wordy", "jules", "spike", "sru", "parker", "sam", "ed", "lets", "greg", "copy", "guys", "sierra", "winnie", "misha",
    "allez", "stay", "keep", "gotta", "put", "reçu", "call", "give", "move", "plaît", "violet", "naomi", "addison", "pete", "cooper", "patient",
    "dell", "vie", "feel", "charlotte", "mieux", "shawn", "gus", "spencer", "case", "dude", "dad", "lassiter", "name", "stop", "sûr", "actually",
    "getting", "around", "place", "tony", "fuckin", "shit", "putain", "père", "house", "mère", "home", "anthony", "paulie", "wanna", "huh", "mother"
    "junior", "kid", "carmela", "nothing", "talking", "night", "uncle", "hear", "father", "maison", "john", "kids", "ted", "marshall", "lily", "barney",
    "robin", "great", "super", "soir", "big", "best", "moment", "iet", "désolé", "truc", "logan", "neptune", "keith", "wallace", "kane", "duncan",
    "lilly", "estce", "savoir", "used", "nuit", "déjà", "long"
])

# Fonction pour corriger les accents
def corriger_accents(texte):
    accents = {
        "\u00c0": "À", "\u00c1": "Á", "\u00c2": "Â", "\u00c3": "Ã", "\u00c4": "Ä", 
        "\u00c5": "Å", "\u00c7": "Ç", "\u00c8": "È", "\u00c9": "É", "\u00ca": "Ê", 
        "\u00cb": "Ë", "\u00cc": "Ì", "\u00cd": "Í", "\u00ce": "Î", "\u00cf": "Ï",
        "\u00d1": "Ñ", "\u00d2": "Ò", "\u00d3": "Ó", "\u00d4": "Ô", "\u00d5": "Õ", 
        "\u00d6": "Ö", "\u00d9": "Ù", "\u00da": "Ú", "\u00db": "Û", "\u00dc": "Ü",
        "\u00e0": "à", "\u00e1": "á", "\u00e2": "â", "\u00e3": "ã", "\u00e4": "ä", 
        "\u00e5": "å", "\u00e7": "ç", "\u00e8": "è", "\u00e9": "é", "\u00ea": "ê", 
        "\u00eb": "ë", "\u00ec": "ì", "\u00ed": "í", "\u00ee": "î", "\u00ef": "ï",
        "\u00f1": "ñ", "\u00f2": "ò", "\u00f3": "ó", "\u00f4": "ô", "\u00f5": "õ", 
        "\u00f6": "ö", "\u00f9": "ù", "\u00fa": "ú", "\u00fb": "û", "\u00fc": "ü",
    }
    for char, replacement in accents.items():
        texte = texte.replace(char, replacement)
    return texte

# Fonction pour traiter un fichier JSON
def traiter_fichier_json(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        data = json.load(fichier)
    
    # Parcourir les éléments de la liste
    for element in data:
        for cle, valeur in element.items():
            if isinstance(valeur, str):
                # Corriger les accents
                valeur = corriger_accents(valeur)
                # Conversion en minuscules
                valeur = valeur.lower()
                # Suppression de la ponctuation
                valeur = re.sub(r'[^\w\s]', '', valeur)
                # Supprimer les mots vides
                mots = re.findall(r'\b\w+\b', valeur)
                mots_filtrés = [mot for mot in mots if mot.lower() not in mots_vides]
                element[cle] = " ".join(mots_filtrés)
    
    # Écrire les données modifiées dans le fichier JSON d'origine
    with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
        json.dump(data, fichier, indent=4, ensure_ascii=False)

    # Afficher un message lorsque le fichier est traité
    print(f'Le fichier {chemin_fichier} a été traité avec succès.')

# Chemin vers le répertoire racine contenant les fichiers JSON
repertoire_racine = 'C:/Users/leogu/Desktop/SAE/output'

# Parcourir tous les fichiers .json dans le répertoire
for dossier_racine, _, fichiers in os.walk(repertoire_racine):
    for fichier in fichiers:
        if fichier.endswith('.json'):
            chemin_fichier = os.path.join(dossier_racine, fichier)
            traiter_fichier_json(chemin_fichier)
