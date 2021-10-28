from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.Nodo import Nodo

class Continue(NodoAST):

    def __init__(self,fila,columna) -> None:
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        return Primitivo("",Tipo(7),0,"","")

    def getArbol(self) -> str:
        return Nodo("continue")