
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo

class If(NodoAST):

    def __init__(self,cuerpoIF:NodoAST,cuerpoElse:NodoAST,exp:NodoAST,fila:int,columna:int) -> None:
        self.cuerpoIF = cuerpoIF
        self.cuerpoElse = cuerpoElse
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno) -> Primitivo:
        Rexp = self.exp.ejecutar(entorno)
        if(Rexp.tipo.esError()):
            TablaSimbolos.insertarError(Rexp.valor,self.fila,self.columna)
            return None
        
        elif(Rexp.tipo.esBool()):
            if(Rexp.valor):
                resCuerpo = self.cuerpoIF.ejecutar(entorno)
                if(resCuerpo is not None):
                    if(resCuerpo.tipo.esBreak()):
                        return resCuerpo
                    elif(resCuerpo.tipo.esContinue()):
                        return resCuerpo
                    elif(resCuerpo.tipo.esReturn()):
                        return resCuerpo
            else:
                if(Rexp.valor!=None):
                    if(self.cuerpoElse is not None):
                        resCuerpo = self.cuerpoElse.ejecutar(entorno)
                        if(resCuerpo is not None):
                            if(resCuerpo.tipo.esBreak()):
                                return resCuerpo
                            elif(resCuerpo.tipo.esContinue()):
                                return resCuerpo
                            elif(resCuerpo.tipo.esReturn()):
                                return resCuerpo
                return None
        else:
            TablaSimbolos.insertarError("Tipo de expresion invalido: \""+Rexp.tipo.getTipo()+"\"",self.fila,self.columna)
            return None
    

    def getArbol(self) -> str:
        nodo = Nodo("If")
        nodo.addHoja(Nodo("if"))
        nodo.addHoja(self.exp.getArbol())
        nodo.addHoja(self.cuerpoIF.getArbol())

        if(self.cuerpoElse is not None):
            nodo.addHoja(Nodo("else"))
            nodo.addHoja(self.cuerpoElse.getArbol())

        return nodo