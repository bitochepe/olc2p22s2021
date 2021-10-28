from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.Primitivos.Tipo import Tipo

class inF(NodoAST):

    def __init__(self,linf:NodoAST,lsup:NodoAST) -> None:
        self.linf = linf
        self.lsup = lsup
        self.error = True

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        lif = self.linf.ejecutar(entorno)
        lsu = self.lsup.ejecutar(entorno)
        
        if(lif.tipo.esError()):
            self.error = True
        elif(lif.tipo.esInt() or lif.tipo.esFloat()):
            self.error = False
        else:
            self.error = True

        if(lsu.tipo.esError()):
            self.error = True
        elif(lsu.tipo.esInt() or lsu.tipo.esFloat()):
            self.error = False
        else:
            self.error = True

        return Primitivo([lif.getValor(),lsu.getValor()],Tipo(-2),0,"","")
    
    def getArbol(self) -> str:
        nodo = Nodo("IN")
        nodo.addHoja(self.linf.getArbol())
        nodo.addHoja(self.lsup.getArbol())
        return nodo