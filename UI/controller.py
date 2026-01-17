import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_year = None
        self._current_team = None

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._model.build_graph(self._current_year)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO
        adiacenti = self._model.fill_from_dd_squadra(self._current_team)
        self._view.txt_risultato.controls.clear()
        for (u,peso) in adiacenti:
            self._view.txt_risultato.controls.append(ft.Text(f"{u.team_code} ({u.name}) - peso {peso}"))
        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO
        path_archi, peso = self._model.percorso(self._current_team)
        self._view.txt_risultato.controls.clear()
        for v, u, peso_arco in path_archi:
           self._view.txt_risultato.controls.append(ft.Text(f"{v.team_code} ({v.name}) -> {u.team_code} ({u.name}) (peso {peso_arco})"))
        self._view.txt_risultato.controls.append(ft.Text(f"Peso totale: {peso}"))
        self._view.update()
    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO

    def handle_fill_dd_anno(self):
        anni = self._model.fill_dd_anno()
        self._view.dd_anno.options.clear()
        for a in sorted(anni):
            option = ft.dropdown.Option(text=str(a), data=a)
            self._view.dd_anno.options.append(option)
        self._view.update()

    def get_selected_year(self,e):
        selected_option = e.control.value
        if selected_option is None:
            self._current_year = None
            return
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break
        self._current_year = found
        self.handle_fill_from_dd_anno()

    def handle_fill_from_dd_anno(self):
        teams_anno_selezionato = self._model.fill_from_dd_anno(self._current_year)
        self._view.dd_squadra.options.clear()
        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(teams_anno_selezionato)}"))
        for t in sorted(teams_anno_selezionato):
            self._view.txt_out_squadre.controls.append(ft.Text(f"{t.team_code} ({t.name})"))
            option = ft.dropdown.Option(text=f"{t.team_code} ({t.name})", data=t)
            self._view.dd_squadra.options.append(option)
        self._view.update()

    def get_selected_team(self,e):
        selected_option = e.control.value
        if selected_option is None:
            self._current_year = None
            return
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break
        self._current_team = found