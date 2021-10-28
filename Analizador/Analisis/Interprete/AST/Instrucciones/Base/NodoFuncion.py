from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo

class NodoFuncion(NodoAST):

    def __init__(self,id,params,cuerpo:Cuerpo) -> None:
        self.id = id
        self.params = params
        self.cuerpo = cuerpo
        pass

    def ejecutar(self, entorno) -> Primitivo:
        entorno.insertarFuncion(self.id,self.params,self.cuerpo)

    def getArbol(self) -> str:
        nodo = Nodo("DECFUNC")
        nodo.addHoja(Nodo(self.id))
        nodo.addHoja(Nodo(str(self.params)))
        nodo.addHoja(self.cuerpo.getArbol())
        return nodo