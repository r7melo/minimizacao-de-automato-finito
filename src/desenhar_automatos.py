from graphviz import Digraph
import json
from IPython.display import display

def desenhar_afd(afd, titulo="Autômato"):
    g = Digraph(format="png")
    g.attr(rankdir='LR', label=titulo, labelloc='t', fontsize='20')
    
    
    for e in afd["estados"]:
        g.node(e, shape='doublecircle' if e in afd["estados_finais"] else 'circle', color='green' if e in afd["estados_finais"] else None)
    
    g.node('', shape='none')
    g.edge('', afd["estado_inicial"])
    
    for origem, trans in afd["transicoes"].items():
        for s, destino in trans.items():
            g.edge(origem, destino, label=s)
    return g
