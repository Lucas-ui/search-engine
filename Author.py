class Author:
    def __init__(self, name):
        self.name = name
        self.nb_docs = 0
        # Objet qui permet de stocker les documents de l'auteur
        self.production = {}

    def add(self, id_doc, document):
        self.production[id_doc] = document
        self.nb_docs += 1

    def taille_moyenne_docs(self):
        # Si l'auteur n'a pas de documents, on ne divise pas par 0
        if not self.production:
            return 0
        total_mots = 0
        for doc in self.production.values():
            # Split permet de couper le texte à chaque espace et len compte le nombre de mots
            total_mots += len(doc.texte.split())
        return total_mots / self.nb_docs

    def __str__(self):
        # .1f permet d'arrondir à 1 chiffre après la virgule
        return f"Auteur : {self.name} - {self.nb_docs} documents - Taille moyenne : {self.taille_moyenne_docs():.1f} mots"