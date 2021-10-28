from typing import List
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Nodo import Nodo

class Cuerpo(NodoAST):

    def __init__(self,instrucciones:List[NodoAST]) -> None:
        self.instrucciones = instrucciones

    def ejecutar(self, entorno) -> Primitivo:
        for x in self.instrucciones:
            if(x is not None):
                aux = x.ejecutar(entorno)
                if(aux!=None):
                    return aux
            
        return None
    
    def getArbol(self) -> str:
        nodo = Nodo("Cuerpo")
        for x in self.instrucciones:
            nodo.addHoja(x.getArbol())
        return nodo