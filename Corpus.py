from Author import Author
from RedditDocument import RedditDocument
from ArxivDocument import ArxivDocument
import pandas as pd
import re

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

    def nettoyer_texte(self, chaine):
        chaine = chaine.lower()
        chaine = chaine.replace('\n', ' ')
        chaine = re.sub(r'[^a-z ]', ' ', chaine)
        return chaine

    def search(self, mot_cle):
        print("Recherche")
        matches = re.finditer(mot_cle, self.tout_le_texte, re.IGNORECASE)
        
        compteur = 0
        for match in matches:
            compteur = compteur + 1
            position_mot = match.start()
            debut_phrase = position_mot - 20
            fin_phrase = match.end() + 20
            
            if debut_phrase < 0:
                debut_phrase = 0
                
            passage = self.tout_le_texte[debut_phrase:fin_phrase]
            print("Trouvé : ... " + passage + " ...")
            
        if compteur == 0:
            print("Mot non trouvé.")

    def concorde(self, expression, taille=20):
        donnees = []
        
        matches = re.finditer(expression, self.tout_le_texte, re.IGNORECASE)
        
        for match in matches:
            gauche = self.tout_le_texte[ match.start()-taille : match.start() ]
            centre = match.group()
            droite = self.tout_le_texte[ match.end() : match.end()+taille ]
            
            ligne = {
                "contexte gauche": gauche,
                "motif trouvé": centre,
                "contexte droit": droite
            }
            donnees.append(ligne)
            
        return pd.DataFrame(donnees)

    def stats(self, n=10):
        print("Statistiques")
        
        texte_propre = self.nettoyer_texte(self.tout_le_texte)
        
        liste_mots = texte_propre.split()
        
        dico_compteur = {}
        for mot in liste_mots:
            if mot in dico_compteur:
                dico_compteur[mot] += 1
            else:
                dico_compteur[mot] = 1
        
        liste_pour_pandas = []
        for mot in dico_compteur:
            nombre = dico_compteur[mot]
            ligne = {"Mot": mot, "Frequence": nombre}
            liste_pour_pandas.append(ligne)
            
        df = pd.DataFrame(liste_pour_pandas)
        
        df = df.sort_values(by="Frequence", ascending=False)
        
        print("Nombre de mots uniques : " + str(len(dico_compteur)))
        print("Top " + str(n) + " des mots :")
        print(df.head(n))