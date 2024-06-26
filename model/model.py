import copy

import networkx as nx

from database.DAO import DAO
from database.DB_connect import DBConnect


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.soluzioneBest = []
        self.costoBest = 0


    def creaGrafo(self, anno, nazione):
        self.grafo.clear()
        self.grafo.add_nodes_from(DAO.getNodi(nazione))
        for u in self.grafo.nodes:
            for v in self.grafo.nodes:
                if u != v:
                    arco = DAO.getArco(anno, u.Retailer_code, v.Retailer_code)
                    if arco != []:
                        self.grafo.add_edge(u, v, weight=arco[0])


    def grafoDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def calcolaVolumeVendita(self):
        listaNodi = []
        for nodo in self.grafo.nodes:
            volume = 0
            for vicino in self.grafo.neighbors(nodo):
                volume += self.grafo[nodo][vicino]["weight"]
            listaNodi.append((volume, nodo))
        listaNodi.sort(reverse=True, key=lambda x: x[0])
        return listaNodi

    def trovaPercorso(self, N):
        self.soluzioneBest = []
        self.costoBest = 0
        for nodo in self.grafo.nodes:
            self.ricorsione([nodo], N)

    def ricorsione(self, parziale, lunMax):
        if len(parziale) == lunMax:
            if parziale[0] == parziale[-1]:
                if self.costoBest(parziale):
                    self.soluzioneBest = copy.deepcopy(parziale)
        else:
            for nodo in self.grafo.neighbors(parziale[-1]):
                if self.soddisfaVincoli(parziale, nodo):
                    parziale.add(nodo)
                    self.ricorsione(parziale, lunMax)
                    parziale.pop()

    def soddisfaVincoli(self, lista, nodo):
        pass

    def costoBest(self, lista):
        pass