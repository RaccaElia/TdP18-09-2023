import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        nazioni = DAO.getNazioni()
        anni = DAO.getAnni()

        self._view._ddmethod.options = list(map(lambda x: ft.dropdown.Option(x), nazioni))
        self._view._ddyear.options = list(map(lambda x: ft.dropdown.Option(x), anni))

    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        anno = int(self._view._ddyear.value)
        nazione = self._view._ddmethod.value
        self._model.creaGrafo(anno, nazione)
        self._view.txtOut.controls.append(ft.Text(f"nodi: {self._model.grafoDetails()[0]}, archi: {self._model.grafoDetails()[1]}"))
        listaNodi = self._model.calcolaVolumeVendita()
        for nodo in listaNodi:
            self._view.txtOut.controls.append(ft.Text(f"retailer: {nodo[1]}, volume: {nodo[0]}"))
        self._view.update_page()

    def handle_search(self, e):
        self._view.txtOut2.controls.clear()
        N = int(self._view.txtSoglia)
        if N < 2:
            self._view.create_alert("vaffanculo")
        else:
            self._model.trovaPercorso(N)
