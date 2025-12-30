import praw
import urllib.request
import urllib.parse
import xmltodict
import ssl
import os
# from dotenv import load_dotenv

from Corpus import Corpus
from RedditDocument import RedditDocument
from ArxivDocument import ArxivDocument
from SearchEngine import SearchEngine

# Permet de charger les variables d'environnement pour ne pas les rendre visibles
# load_dotenv()

# Une seule instance corpus pour tout le programme
corpus = Corpus("Corpus")

print("Chargement des données Reddit")

# Projet professionnel : utiliser des variables d'environnement serait une meilleure pratique
# reddit = praw.Reddit(
#     client_id=os.getenv("REDDIT_CLIENT_ID"),
#     client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
#     user_agent=os.getenv("REDDIT_USER_AGENT")
# )

reddit = praw.Reddit(
    client_id="ag4KNe12bqjztncUW3zlRw",
    client_secret="bMJ0U_O5MgI-XV0MAcL-AfRicGCRNA",
    user_agent="WebScraping"
)

theme = 'climate'
posts = reddit.subreddit(theme).hot(limit=10)

# On parcourt les posts trouvés sur le thème renseigné
for post in posts:
    # Si post sans texte, le titre sera le contenu
    if post.selftext:
        contenu = post.selftext
    else:
        contenu = post.title
    
    # Si le contenu est trop court, on passe à la suite
    if len(contenu) < 100:
        continue

    doc = RedditDocument(
        titre=post.title,
        auteur=str(post.author),
        date=str(post.created_utc),
        url=post.url,
        texte=contenu,
        nb_comments=post.num_comments
    )

    print(f"Récupération Reddit : {doc.titre[:50]}")
    corpus.add_document(doc)

print("Chargement des données Arxiv")

mot_cle = 'electron'
# Gère les caractères spéciaux ou les espaces dans la requête
mot_cle_encode = urllib.parse.quote(mot_cle)
url = f"http://export.arxiv.org/api/query?search_query=all:{mot_cle_encode}&start=0&max_results=10"

# Permet éviter les bugs liés au certificat
context = ssl._create_unverified_context()
data = urllib.request.urlopen(url, context=context).read().decode('utf-8')
dico_xml = xmltodict.parse(data)

# On vérifie qu'il y a bien du contenu avant de le traiter
if "entry" in dico_xml["feed"]:
    entries = dico_xml["feed"]["entry"]
    
    # On force la transformation en liste pour que ça fonctionne toujours
    if not isinstance(entries, list):
        entries = [entries]

    for entry in entries:
        contenu = entry['summary']

        if len(contenu) < 100:
            continue

        info_auteur = entry['author']
        liste_co_auteurs = []
        nom_auteur = "Inconnu"

        # Gère les auteurs, s'il y en a plusieurs ou non
        if isinstance(info_auteur, list):
            nom_auteur = info_auteur[0]['name']
            for a in info_auteur[1:]:
                liste_co_auteurs.append(a['name'])
        else:
            nom_auteur = info_auteur['name']

        doc = ArxivDocument(
            titre=entry['title'],
            auteur=nom_auteur,
            date=entry['published'],
            url=entry['id'],
            texte=contenu,
            co_authors=liste_co_auteurs
        )
        
        print(f"Récupération Arxiv : {doc.titre[:50]}")
        corpus.add_document(doc)
else:
    print("Aucun résultat trouvé sur Arxiv.")

print(f"Nombre de documents validés : {len(corpus.documents)}")
print(f"Nombre d'auteurs identifiés : {len(corpus.authors)}")

# Enregistre le corpus dans le dossier pour pouvoir réutiliser les données
corpus.save("corpus.csv")

if len(corpus.documents) > 0:
    print("\nExemple du premier document :")
    premier_doc = list(corpus.documents.values())[0]
    print(premier_doc)

# Statistiques
corpus.stats(n=5)

# Initialisation et test du moteur de recherche
moteur = SearchEngine(corpus)

mot = input("\nEntrez un mot à chercher (ex: climate, energy) : ")
df_res = moteur.search(mot)

if not df_res.empty:
    print(f"\nRésultats pour '{mot}':")
    print(df_res)
else:
    print("Aucun résultat trouvé.")