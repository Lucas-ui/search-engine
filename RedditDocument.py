from Document import Document

class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_comments):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_comments = nb_comments

    def get_nb_comments(self):
        return self.nb_comments

    def set_nb_comments(self, nb):
        self.nb_comments = nb

    def getType(self):
        return "Reddit"

    def __str__(self):
        return f"{self.titre} ({self.auteur}) — {self.nb_comments} commentaires"
