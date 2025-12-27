from Author import Author
from RedditDocument import RedditDocument
from ArxivDocument import ArxivDocument
import pandas as pd

class Corpus:
    instance_unique = None

    def __new__(cls, nom):
        if cls.instance_unique is None:
            cls.instance_unique = super().__new__(cls)
            cls.instance_unique.nom = nom
            cls.instance_unique.documents = {}
            cls.instance_unique.authors = {}
            cls.instance_unique.id_document = 0
            cls.instance_unique.tout_le_texte = ""
        return cls.instance_unique

    def add_document(self, document):
        self.documents[self.id_document] = document
        self.tout_le_texte += " " + document.texte
        
        nom = document.auteur
        if nom not in self.authors:
            self.authors[nom] = Author(nom)
        self.authors[nom].add(self.id_document, document)

        self.id_document += 1

    def afficher_documents(self, n_docs=-1):
        cpt = 0
        for doc in self.documents.values():
            print(doc)
            cpt += 1
            if n_docs > 0 and cpt >= n_docs:
                break

    def save(self, filename="corpus.csv"):
        data = []
        for id_doc, doc in self.documents.items():
            info_sup = ""
            if doc.getType() == "Reddit":
                info_sup = doc.nb_comments
            else:
                info_sup = ",".join(doc.co_authors)

            row = {
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte,
                "type": doc.getType(),
                "info_sup": info_sup
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(filename, sep="\t", index=False)
        print(f"Sauvegardé dans {filename}")

    def load(self, filename="corpus.csv"):
        df = pd.read_csv(filename, sep="\t")
        
        self.documents = {}
        self.authors = {}
        self.id_document = 0
        self.tout_le_texte = ""

        for i, row in df.iterrows():
            
            if row["type"] == "Reddit":
                doc = RedditDocument(
                    row["titre"], row["auteur"], row["date"], 
                    row["url"], row["texte"], row["info_sup"]
                )
            else:
                info = str(row["info_sup"])
                if info == "nan":
                    co_auteurs = []
                else:
                    co_auteurs = info.split(",")
                
                doc = ArxivDocument(
                    row["titre"], row["auteur"], row["date"], 
                    row["url"], row["texte"], co_auteurs
                )
            self.add_document(doc)
        print("Chargement terminé.")