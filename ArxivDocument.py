from Document import Document

# ArvixDocument hérite de Document, il récupère tout son contenu
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_authors):
        # Constructeur de la classe Document pour gérer les différents éléments
        super().__init__(titre, auteur, date, url, texte)
        # On ajoute juste ce qui est spécifique à Arxiv
        self.co_authors = co_authors

    def get_co_authors(self):
        return self.co_authors

    def set_co_authors(self, co_authors):
        self.co_authors = co_authors

    # Permet de différencier les documents entre Arxiv et Reddit
    def getType(self):
        return "Arxiv"

    def __str__(self):
        # Permet de transformer la liste en chaîne de caractères, simplifie l'affichage
        co = ", ".join(self.co_authors)
        # On affiche les co-auteurs que s'il y en a
        return f"{self.titre} ({self.auteur}) — Co-auteurs : {co}" if co else f"{self.titre} ({self.auteur})"
