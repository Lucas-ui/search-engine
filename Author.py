class Author:
    def __init__(self, name):
        self.name = name
        self.nb_docs = 0
        self.production = {}

    def add(self, id_doc, document):
        self.production[id_doc] = document
        self.nb_docs += 1

    def taille_moyenne_docs(self):
        if not self.production:
            return 0
        total_mots = 0
        for doc in self.production.values():
            total_mots += len(doc.texte.split())
        return total_mots / self.nb_docs

    def __str__(self):
        return f"Auteur : {self.name} - {self.nb_docs} documents - Taille moyenne : {self.taille_moyenne_docs():.1f} mots"