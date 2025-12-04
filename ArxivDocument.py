from Document import Document

class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_authors):
        super().__init__(titre, auteur, date, url, texte)
        self.co_authors = co_authors

    def get_co_authors(self):
        return self.co_authors

    def set_co_authors(self, co_authors):
        self.co_authors = co_authors

    def getType(self):
        return "Arxiv"

    def __str__(self):
        co = ", ".join(self.co_authors)
        return f"{self.titre} ({self.auteur}) — Co-auteurs : {co}" if co else f"{self.titre} ({self.auteur})"
