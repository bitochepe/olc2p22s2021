from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.Primitivos.Tipo import Tipo

class Struct(NodoAST):

    def __init__(self,id,muteable:bool,atributos):
        self.id = id
        self.muteable  = muteable
        self.atributos = atributos

    def ejecutar(self, entorno):
        c3d = ""
        for x in self.atributos:
            aux = x.ejecutar(entorno)

    def getArbol(self):
        nodo = Nodo("Primitivo")
        nodo.addHoja(Nodo(self.valor))
        return nodo


