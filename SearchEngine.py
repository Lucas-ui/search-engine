import pandas as pd

class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocabulaire = set()
        self.tf_matrix = []
        
        self.construire_matrice()

    def construire_matrice(self):
        for doc in self.corpus.documents.values():
            
            texte = self.corpus.nettoyer_texte(doc.texte)
            mots = texte.split()
            
            compteur = {}
            for mot in mots:
                if mot in compteur:
                    compteur[mot] += 1
                else:
                    compteur[mot] = 1
                
                self.vocabulaire.add(mot)
            
            self.tf_matrix.append({
                "doc_obj": doc,
                "stats": compteur
            })
            
        print(f"Vous pouvez utiliser le moteur : ({len(self.vocabulaire)} mots connus)")

    def search(self, requete, n_docs=5):
        requete_propre = self.corpus.nettoyer_texte(requete)
        mots_recherche = requete_propre.split()
        
        resultats = []
        
        for ligne in self.tf_matrix:
            doc = ligne["doc_obj"]
            stats = ligne["stats"]
            score = 0
            
            for mot in mots_recherche:
                if mot in stats:
                    score += stats[mot]
            
            if score > 0:
                resultats.append({
                    "Titre": doc.titre,
                    "Auteur": doc.auteur,
                    "Score": score,
                    "Type": doc.getType()
                })
        
        df = pd.DataFrame(resultats)
        
        if not df.empty:
            df = df.sort_values(by="Score", ascending=False)
            return df.head(n_docs)
        else:
            return pd.DataFrame()