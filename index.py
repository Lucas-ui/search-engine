import praw
import urllib.request
import urllib.parse
import xmltodict
import ssl
import os
from dotenv import load_dotenv

from Corpus import Corpus
from RedditDocument import RedditDocument
from ArxivDocument import ArxivDocument

load_dotenv()

mon_corpus = Corpus("Mon corpus")

print("Chargement des données Reddit")

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

theme = 'climate'
posts = reddit.subreddit(theme).hot(limit=10)

for post in posts:
    if post.selftext:
        contenu = post.selftext
    else:
        contenu = post.title
    
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
    mon_corpus.add_document(doc)

print("Chargement des données Arxiv")

mot_cle = 'electron'
mot_cle_encode = urllib.parse.quote(mot_cle)
url = f"http://export.arxiv.org/api/query?search_query=all:{mot_cle_encode}&start=0&max_results=10"

context = ssl._create_unverified_context()
data = urllib.request.urlopen(url, context=context).read().decode('utf-8')
dico_xml = xmltodict.parse(data)

if "entry" in dico_xml["feed"]:
    entries = dico_xml["feed"]["entry"]
    
    if not isinstance(entries, list):
        entries = [entries]

    for entry in entries:
        contenu = entry['summary']

        if len(contenu) < 100:
            continue

        info_auteur = entry['author']
        liste_co_auteurs = []
        nom_auteur = "Inconnu"

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
        mon_corpus.add_document(doc)
else:
    print("Aucun résultat trouvé sur Arxiv.")

print(f"Nombre de documents validés : {len(mon_corpus.documents)}")
print(f"Nombre d'auteurs identifiés : {len(mon_corpus.authors)}")

mon_corpus.save("./data/corpus.csv")

if len(mon_corpus.documents) > 0:
    print("\nExemple du premier document :")
    premier_doc = list(mon_corpus.documents.values())[0]
    print(premier_doc)