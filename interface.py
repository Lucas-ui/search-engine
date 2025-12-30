from dash import *
from Corpus import Corpus
from SearchEngine import SearchEngine

corpus = Corpus("Corpus")

corpus.load("corpus.csv")

moteur = SearchEngine(corpus)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Moteur de recherche"),
    
    dcc.Input(id='input-recherche', type='text', value=''),
    html.Button('Valider', id='btn-valider', n_clicks=0),
    
    html.Br(), html.Br(),
    
    html.Div(id='zone-resultats')
])

@callback(
    Output('zone-resultats', 'children'),
    Input('btn-valider', 'n_clicks'),
    State('input-recherche', 'value'),
)

def lancer_recherche(n_clicks, texte):
    df = moteur.search(texte, n_docs=5)
    
    if df.empty:
        return "Aucun résultat."
    
    liste_affichage = []
    for index, row in df.iterrows():
        ligne = html.P(f"- {row['Titre']} (Score: {row['Score']})")
        liste_affichage.append(ligne)
        
    return liste_affichage

if __name__ == '__main__':
    app.run()