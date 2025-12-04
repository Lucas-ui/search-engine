import praw
import urllib.request
import xmltodict
import pandas as pd
import ssl
from Document import Document
from Author import Author
# 3 VERSIONS A RENDRE POUR JANVIER 1) JUSQUAU TD 5 2) JUSQUAU TD 10 3) PROJET FINAL
reddit = praw.Reddit(
    client_id='ag4KNe12bqjztncUW3zlRw',
    client_secret='bMJ0U_O5MgI-XV0MAcL-AfRicGCRNA',
    user_agent='WebScraping'
)

documents = {}
authors = {}
id_doc = 1

theme = 'climate'
hot_posts = reddit.subreddit(theme).hot(limit=10)

for post in hot_posts:
    doc = Document(
        titre=post.title,
        auteur=str(post.author),
        date=str(post.created_utc),
        url=post.url,
        texte=post.selftext if post.selftext else post.title
    )
    documents[id_doc] = doc

    auteur_nom = doc.auteur
    if auteur_nom not in authors:
        authors[auteur_nom] = Author(auteur_nom)
    authors[auteur_nom].add(id_doc, doc)

    id_doc += 1

print(f"Nombre de documents Reddit : {len(documents)}")

query = 'electron'
encoded_query = urllib.parse.quote(query)
url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results=10"

context = ssl._create_unverified_context()
data = urllib.request.urlopen(url, context=context).read().decode('utf-8')
parseData = xmltodict.parse(data)

if "entry" in parseData["feed"]:
    entries = parseData["feed"]["entry"]
    entries = entries if isinstance(entries, list) else [entries]

    for entry in entries:
        auteur_info = entry['author']
        if type(auteur_info) == list:
            auteur = auteur_info[0]['name']
        else:
            auteur = auteur_info['name']

        doc = Document(
            titre=entry['title'],
            auteur=auteur,
            date=entry['published'],
            url=entry['id'],
            texte=entry['summary']
        )
        documents[id_doc] = doc

        if auteur not in authors:
            authors[auteur] = Author(auteur)
        authors[auteur].add(id_doc, doc)

        id_doc += 1
else:
    print("Aucun résultat Arxiv trouvé pour cette requête.")

print(f"Nombre total de documents (Reddit + Arxiv) : {len(documents)}")

print("\nExemple d’un document :")
un_doc = list(documents.values())[0]
un_doc.afficher()

docs_list = []
for doc_id, doc in documents.items():
    docs_list.append({
        "id": doc_id,
        "titre": doc.titre,
        "auteur": doc.auteur,
        "date": doc.date,
        "url": doc.url,
        "texte": doc.texte
    })

# df_docs = pd.DataFrame(docs_list)
# df_docs.to_csv("corpus.tsv", sep="\t", index=False)
# print("\nCorpus sauvegardé dans 'corpus.tsv'")

nom_recherche = input("\nEntrez le nom d'un auteur pour voir ses stats : ")

if nom_recherche in authors:
    author = authors[nom_recherche]
    nb_docs = author.nb_docs
    total_mots = 0
    for doc in author.production.values():
        nb_mots = len(doc.texte.split())
    total_mots += nb_mots
    taille_moyenne = total_mots / nb_docs if nb_docs > 0 else 0

    print(f"Auteur : {author.name}")
    print(f"Nombre de documents : {nb_docs}")
    print(f"Taille moyenne des documents (en mots) : {taille_moyenne:.2f}")
else:
    print("Auteur non trouvé.")


# exemple regex
# motif = re.compile("python");
# matches = motif.finditer(texte);
# for m in matches:
    # print(f"...")