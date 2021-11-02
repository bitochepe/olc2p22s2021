from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.Nodo import Nodo

class Break(NodoAST):

    def __init__(self,fila,columna) -> None:
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        c3d = ""
        if(len(TablaSimbolos.display)>0):
            c3d += "goto "+TablaSimbolos.display[0][1]+";\n"
        else:
            TablaSimbolos.insertarError("Sentencia continue fuera de ciclo",self.fila,self.columna)
        return Primitivo("",Tipo(8),0,"","",c3d)

    def getArbol(self) -> str:
        return Nodo("break")