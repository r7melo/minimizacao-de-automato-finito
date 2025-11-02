import json
import pandas as pd
from tools import get_raw_file, get_processed_file

import sys
from pathlib import Path
sys.path.append(str(Path("../data/").resolve()))

class eAFN():

    def __init__(self, filename):
        
        self.data = None
        self.df_transicoes = None


        with open(get_raw_file(filename), "r",  encoding="utf-8") as f:
            self.data = json.load(f)

            self.df_transicoes = pd.DataFrame(self.data["transicoes"]).T


    def fechoEpsilon(self, estado, fechamento=None):
    
        if fechamento is None:
            fechamento = set()
        
        fechamento.add(estado)

        proximos_estados = self.df_transicoes.T[estado]["ε"]
        
        for s in proximos_estados:
            if s not in fechamento:
                self.fechoEpsilon(s, fechamento)
        
        return fechamento
    
    def novoDelta(self, qi, x):
        deltaEpsilonQi = self.fechoEpsilon(qi)
        conjunto_x_mv = [set(self.df_transicoes[x][s]) for s in deltaEpsilonQi]
        conjunto_transicoes_x = set().union(*conjunto_x_mv)
        conjunto_x_epsilon = [self.fechoEpsilon(r) for r in conjunto_transicoes_x]
        novas_transicoes_x = set().union(*conjunto_x_epsilon)
        return list(novas_transicoes_x)
    
    def geraAFN(self):

        # gerando copia para atualização
        novo_data = self.data.copy()

        # Conjunto de estados finais
        estados_finais = set(self.data["estados_finais"])

        # Novas transições
        novas_transicoes_AFN = {}
        novos_estados_finais = set()

        for t in self.df_transicoes.index.to_list():
            novas_transicoes_AFN[t] = {}
            for a in self.data["alfabeto"]:
                novas_transicoes_AFN[t][a] = self.novoDelta(t, a)

            if self.fechoEpsilon(t) & estados_finais:
                novos_estados_finais.add(t)

        # Atualização do modelo
        novo_data["transicoes"] = novas_transicoes_AFN
        novo_data["estados_finais"] = list(novos_estados_finais)

        return novo_data
    
    def save(self, novo_data, filename):

        # Salvar o JSON
        with open(get_processed_file(filename), "w",  encoding="utf-8") as f:
            json.dump(novo_data, f, indent=4)

        return "Salvo com sucesso!"

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False, indent=4)