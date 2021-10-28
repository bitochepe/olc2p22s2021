from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.Nodo import Nodo

class Return(NodoAST):

    def __init__(self,exp:NodoAST,fila,columna) -> None:
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        if(self.exp is not None):
            resExp = self.exp.ejecutar(entorno)
            if(resExp.tipo.esError()):
                TablaSimbolos.insertarError("Error en sentencia Return: "+str(resExp.getValor()),self.fila,self.columna)
                return None
            return Primitivo(resExp,Tipo(6),0,"","")
        return Primitivo(None,Tipo(6),0,"","")
        

    def getArbol(self) -> str:
        return Nodo("return")