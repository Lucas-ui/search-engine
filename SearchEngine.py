import pandas as pd

class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocabulaire = set() # Evite les doublons
        self.tf_matrix = [] # Matrice
        
        # Construction de la matrice
        self.construire_matrice()

    def construire_matrice(self):
        # On parcourt chacun des documents
        for doc in self.corpus.documents.values():
            
            # Permet de rendre le contenu "propre", en minuscule, sans ponctuation
            texte = self.corpus.nettoyer_texte(doc.texte)
            mots = texte.split()
            
            # On compte combien de fois chaque mot apparaît dans le document
            compteur = {}
            for mot in mots:
                if mot in compteur:
                    compteur[mot] += 1
                else:
                    compteur[mot] = 1
                
                self.vocabulaire.add(mot)
            
            # On ajoute à la matrice le document et le nombre de mots
            self.tf_matrix.append({
                "doc_obj": doc,
                "stats": compteur
            })
            
        print(f"Vous pouvez utiliser le moteur : ({len(self.vocabulaire)} mots connus)")

    def search(self, requete, n_docs=5):
        # On nettoie la requête de l'utilisateur (comme pour les textes)
        requete_propre = self.corpus.nettoyer_texte(requete)
        mots_recherche = requete_propre.split()
        
        resultats = []
        
        # On compare la requête avec chacun des documents de la matrice
        for ligne in self.tf_matrix:
            doc = ligne["doc_obj"]
            stats = ligne["stats"]
            score = 0
            
            # Pour le score, on l'incrémente lorsqu'on voit le mot cherché
            for mot in mots_recherche:
                if mot in stats:
                    score += stats[mot]
            
            # Si le document contient au moins un des mots, on le garde
            if score > 0:
                resultats.append({
                    "Titre": doc.titre,
                    "Auteur": doc.auteur,
                    "Score": score,
                    "Type": doc.getType()
                })
        
        # Utilisation de Pandas pour la mise en forme
        df = pd.DataFrame(resultats)
        
        if not df.empty:
            # Les plus gros scores en premier
            df = df.sort_values(by="Score", ascending=False)
            return df.head(n_docs)
        else:
            return pd.DataFrame()