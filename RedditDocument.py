from Document import Document

# RedditDocument hérite de Document, il récupère tout le contenu
class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_comments):
        # Constructeur de la classe Document pour gérer les différents éléments
        super().__init__(titre, auteur, date, url, texte)
        # On ajoute juste ce qui est spécifique à Arxiv
        self.nb_comments = nb_comments

    def get_nb_comments(self):
        return self.nb_comments

    def set_nb_comments(self, nb):
        self.nb_comments = nb

    # Permet de différencier les documents entre Arxiv et Reddit
    def getType(self):
        return "Reddit"

    def __str__(self):
        return f"{self.titre} ({self.auteur}) — {self.nb_comments} commentaires"
