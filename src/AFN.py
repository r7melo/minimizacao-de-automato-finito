import json
import pandas as pd
import re
from tools import get_raw_file, get_processed_file

import sys
from pathlib import Path
sys.path.append(str(Path("../data/").resolve()))

class AFN():

    def __init__(self, filename):
        
        self.data = None
        self.df_transicoes = None


        with open(get_raw_file(filename), "r",  encoding="utf-8") as f:
            self.data = json.load(f)

            self.df_transicoes = pd.DataFrame(self.data["transicoes"]).T


    def gera_pi(self, pi, transicao): # Ex.: ('q0',)

        novo_pi = set()
        
        for estado in pi:
            qiqu = set(self.df_transicoes.T[estado][transicao])
            novo_pi = novo_pi.union(qiqu)

        novo_pi_l = list(novo_pi)
        novo_pi_l.sort()

        novo_pi = tuple(novo_pi_l)

        return novo_pi

    def gera_transicoes(self, pi, pilha=None, novas_transicoes=None):
    
        if pilha is None:
            pilha = set()

        if novas_transicoes is None:
            novas_transicoes = {}
            
        if pi in pilha:
            return novas_transicoes
        else:
            pilha.add(pi)
            
        novas_transicoes[pi] = {}
        for transicao in self.df_transicoes.T.index.to_list():
            novo_pi = self.gera_pi(pi, transicao)
            novas_transicoes[pi][transicao] = novo_pi
            self.gera_transicoes(novo_pi, pilha, novas_transicoes)

        return novas_transicoes   


    
    def geraAFD(self):

        estado_inicial = ('q0',)
        nt = self.gera_transicoes(estado_inicial)
        nt

        # Função que faz a redução de '('q0', 'q1')' => 'q0q1'
        ct = lambda s: re.sub(r"[()',\s]", "", str(s))

        # DataFrame criando a partir de um novo objeto reduzido e válido
        df_nova_transicoes = pd.DataFrame.from_dict({
            
            ct(index): {
                transicao: ct(estado)            
                
                for transicao, estado in value.items()
            }
            
            for index, value in nt.items()
            
        }, orient="index")


        # Dicionário para tradução dos novos estados
        dtraduz = {
            estado: f"p{i}*" if any([qf in estado for qf in self.data["estados_finais"]]) else f"p{i}"
            for i, estado in enumerate(df_nova_transicoes.index.to_list())
        }

        AFD_transicoes = df_nova_transicoes.rename(index=dtraduz).replace(dtraduz)
        AFD_transicoes

        # Recuperando estados finais
        AFD_estados_finais = [estado for _, estado in dtraduz.items() if '*' in estado]
        AFD_estados_finais

        # Montando modelo por partes
        data_novo = self.data.copy()
        data_novo["estados"] = AFD_transicoes.index.to_list()
        data_novo["estado_inicial"] = AFD_transicoes.index[0]
        data_novo["estados_finais"] = AFD_estados_finais
        data_novo["transicoes"] = AFD_transicoes.T.to_dict()
        data_novo


        return data_novo
    
    def save(self, novo_data, filename):

        # Salvar o JSON
        with open(get_processed_file(filename), "w",  encoding="utf-8") as f:
            json.dump(novo_data, f, indent=4)

        return "Salvo com sucesso!"

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False, indent=4)