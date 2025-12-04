class Document:
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    def afficher(self):
        print("Titre :", self.titre)
        print("Auteur :", self.auteur)
        print("Date :", self.date)
        print("URL :", self.url)
        print("Texte :", self.texte)

    def __str__(self):
        return f"{self.titre} ({self.auteur})"
