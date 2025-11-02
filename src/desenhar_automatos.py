from graphviz import Digraph

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

def desenhar_afn(afn, titulo="Autômato Não Determinístico"):
    g = Digraph(format="png")
    g.attr(rankdir='LR', label=titulo, labelloc='t', fontsize='20')

    # Estados
    for e in afn["estados"]:
        g.node(e, shape='doublecircle' if e in afn["estados_finais"] else 'circle', 
               color='green' if e in afn["estados_finais"] else None)

    # Estado inicial fictício
    g.node('', shape='none')
    g.edge('', afn["estado_inicial"])

    # Transições (cada símbolo pode ir para vários estados)
    for origem, trans in afn["transicoes"].items():
        for simbolo, destinos in trans.items():
            for destino in destinos:
                g.edge(origem, destino, label=simbolo)

    return g
