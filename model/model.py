import networkx as nx
from database.dao import DAO
from operator import itemgetter

class Model:
    def __init__(self):
        self.team_per_anno = DAO.getTeams()
        self.G = nx.Graph()
        #self._dizionario_team = {}

    def fill_dd_anno(self):
        anni = []
        for anno in self.team_per_anno:
            anni.append(anno)
        return anni

    def fill_from_dd_anno(self,anno):
        teams_anno_selezionato = []
        for team in self.team_per_anno[anno]:
            teams_anno_selezionato.append(team)
        return teams_anno_selezionato

    def build_graph(self, anno):
        self.G.clear()
        nodes = self.team_per_anno[anno]
        for team in nodes:
            #self._dizionario_team[team.id] = team
            self.G.add_node(team)
        if anno <= 1984:
            for v in self.G.nodes():
                for u in self.G.nodes():
                    if not self.G.has_edge(u, v) and v.id != u.id:
                        self.G.add_edge(v, u, peso=0)
        else:
            salario_per_team = DAO.get_peso_archi(anno)
            for v in self.G.nodes():
                salario_v = salario_per_team[v.id]
                for u in self.G.nodes():
                    if not self.G.has_edge(u, v) and v.id != u.id:
                        salario_u = salario_per_team[u.id]
                        salario_tot = salario_v + salario_u
                        self.G.add_edge(v, u, peso=salario_tot)

    def fill_from_dd_squadra(self, v):
        adiacenti_ordinati = self.ordina_vicini(v)
        return adiacenti_ordinati

    def percorso(self, v):
        self.best_path_archi = []
        self.best_peso = 0
        self.k_archi = 3

        visitati = set()
        visitati.add(v.id)
        path_corrente = [v]
        self.ricorsione(path_corrente, 0,float("inf"), visitati, [])
        return self.best_path_archi, self.best_peso

    def ricorsione(self, path_corrente, peso_corrente, peso_ultimo_arco, visitati, path_archi):
        if peso_corrente > self.best_peso:
            self.best_peso = peso_corrente
            self.best_path_archi = list(path_archi)
        ultimo_nodo = path_corrente[-1]
        vicini = self.ordina_vicini(ultimo_nodo)
        candidati_validi = []
        for vicino, peso in vicini:
            if (vicino.id not in visitati) and (peso < peso_ultimo_arco):
                candidati_validi.append((vicino, peso))
        for vicino, peso in candidati_validi[0:self.k_archi]:
            visitati.add(vicino.id)
            path_corrente.append(vicino)
            path_archi.append((ultimo_nodo, vicino, peso))
            self.ricorsione(path_corrente, peso_corrente + peso, peso, visitati, path_archi)
            path_corrente.pop()
            visitati.remove(vicino.id)

    def ordina_vicini(self,v):
        lista_vicini = []
        for neighbor in self.G.neighbors(v):
            peso = self.G[v][neighbor]['peso']
            lista_vicini.append((neighbor, peso))
        return sorted(lista_vicini, key=itemgetter(1), reverse=True)