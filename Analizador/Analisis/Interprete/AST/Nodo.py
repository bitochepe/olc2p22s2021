
class Nodo:

    def __init__(self,dato) -> None:
        self.dato = dato
        self.hojas = []

    def addHoja(self,dato):
        self.hojas.append(dato)

    def getDato(self):
        return self.dato

    def getHojas(self):
        return self.hojas