import requests
import os

# Liste des noms de séries TV
series = [
"24", "90210", "alias", "angel", "battlestargalactica", "betteroffted", "bionicwoman", "blade", "bloodties", "bones", "breakingbad", 
"buffy", "burnnotice", "californication", "caprica", "charmed", "chuck", "coldcase", "community", "criminalminds", "cupid", "daybreak", 
"demons", "desperatehousewives", "dexter", "dirt", "dirtysexymoney", "doctorwho", "dollhouse", "eleventhhour", "entourage", "eureka", 
"extras", "fearitself", "flashforward", "flashpoint", "flightoftheconchords", "fridaynightlights", "friends", "fringe", "futurama", 
"garyunmarried", "ghostwhisperer", "gossipgirl", "greek", "greysanatomy", "heroes", "house", "howimetyourmother", "intreatment", "invasion", 
"jake", "jekyll", "jericho", "johnfromcincinnati", "knightrider", "kylexy", "legendoftheseeker", "leverage", "lietome", "lost", "madmen", 
"mastersofscifi", "medium", "melroseplace", "mental", "merlin", "moonlight", "mynameisearl", "ncis", "ncislosangeles", "niptuck", "onetreehill", 
"oz", "painkillerjane", "primeval", "prisonbreak", "privatepractice", "psych", "pushingdaisies", "raines", "reaper", "robinhood", "rome", "samanthawho", 
"sanctuary", "scrubs", "sexandthecity", "sixfeetunder", "skins", "smallville", "sonsofanarchy", "southpark", "spaced", "stargateatlantis", "stargatesg1", 
"stargateuniverse", "supernatural", "swingtown", "the4400", "thebigbangtheory", "theblackdonnellys", "thekillpoint", "thelostroom", "thementalist", 
"thenine", "theoc", "thepretender", "theriches", "thesarahconnorchronicles", "theshield", "thesopranos", "thetudors", "thevampirediaries", "thewire", 
"torchwood", "traveler", "trucalling", "trueblood", "uglybetty", "veronicamars", "weeds", "whitechapel", "womensmurderclub", "xfiles"
"battlestar-galactica", "better-off-ted", "bionic-woman", "blood-ties", "breaking-bad", "burn-notice", "criminal-minds", 
"desperate-housewives", "dirty-sexy-money", "doctor-who", "eleventh-hour", "fear-itself", "flight-of-the-conchords", "friday-night-lights", 
"gary-unmarried", "ghost-whisperer", "gossip-girl", "greys-anatomy", "how-i-met-your-mother", "in-treatment", "john-from-cincinnati", "knight-rider", 
"kyle-xy", "legend-of-the-seeker", "lie-to-me", "masters-of-scifi", "melrose-place", "my-name-is-earl", "ncis-los-angeles", "one-tree-hill", 
"painkiller-jane", "prison-break", "private-practice", "pushing-daisies", "samantha-who", "sex-and-the-city", "six-feet-under", "sons-of-anarchy", 
"stargate-atlantis", "stargate-sg1", "the-4400", "the-big-bang-theory", "the-black-donnellys", "the-kill-point", "the-lost-room", "the-mentalist", 
"the-nine", "the-oc", "the-pretender", "the-riches", "the-sarah-connor-chronicles", "the-shield", "the-sopranos", "the-tudors", "the-vampire-diaries", 
"the-wire", "tru-calling", "true-blood", "ugly-betty", "veronica-mars", "womens-murder-club"]

# Créez un dossier pour stocker les affiches si ce n'est pas déjà fait
if not os.path.exists("images"):
    os.makedirs("images")

# Fonction pour récupérer l'affiche d'une série TV depuis TheTVDB
def get_tv_show_poster_from_thetvdb(tv_show_name):
    api_key = '1f73bff8-6183-4139-9450-a7a821c0b1c5'
    url = f"https://api.thetvdb.com/search/series?name={tv_show_name}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            series_id = data["data"][0]["id"]
            series_url = f"https://api.thetvdb.com/series/{series_id}/images/query?keyType=poster"
            response = requests.get(series_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    poster_url = data["data"][0]["fileName"]
                    return f"https://www.thetvdb.com/banners/{poster_url}"
    
    return None

# Récupérez les affiches pour chaque série et sauvegardez-les dans le dossier "posters"
for tv_show in series:
    print(f"Récupération de l'affiche de {tv_show}...")
    poster_url = get_tv_show_poster_from_thetvdb(tv_show)
    if poster_url:
        response = requests.get(poster_url)
        if response.status_code == 200:
            with open(f"C:/Users/leogu/Desktop/SAE/images/{tv_show}.jpg", "wb") as file:
                file.write(response.content)
                print(f"Affiche de {tv_show} sauvegardée avec succès.")
    else:
        print(f"Impossible de trouver l'affiche de {tv_show}.")
