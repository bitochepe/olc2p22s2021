
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Primitivo:
    def __init__(self, valor, tipo:Tipo, dimension, EV,EF,c3d):
        self.dimension = dimension
        self.tipo = tipo
        self.valor = valor
        self.EV = EV
        self.EF = EF
        self.c3d = c3d

    def esArray(self):
        return self.dimension > 0

    def getValor(self):
        return self.valor

    def getEV(self):
        return self.EV

    def getEF(self):
        return self.EF
    
    def getc3d(self):
        return self.c3d

    def getArbol(self):
        nodo = Nodo("Primitivo")
        nodo.addHoja(Nodo(self.valor))
        return nodo