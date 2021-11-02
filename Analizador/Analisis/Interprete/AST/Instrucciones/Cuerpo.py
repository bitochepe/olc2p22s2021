from os import times
from typing import List
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Nodo import Nodo

class Cuerpo(NodoAST):

    def __init__(self,instrucciones:List[NodoAST]) -> None:
        self.instrucciones = instrucciones

    def ejecutar(self, entorno) -> Primitivo:
        c3d = ""
        for x in self.instrucciones:
            if(x is not None):
                aux = x.ejecutar(entorno)
                c3d += aux.getc3d() +"\n"
        return Primitivo("",Tipo(0),0,"","",c3d)
    
    def getArbol(self) -> str:
        nodo = Nodo("Cuerpo")
        for x in self.instrucciones:
            nodo.addHoja(x.getArbol())
        return nodo