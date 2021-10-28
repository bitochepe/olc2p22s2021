from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo

class While(NodoAST):

    def __init__(self, exp:NodoAST, cuerpo:Cuerpo, fila, column) -> None:
        self.exp = exp
        self.cuerpo = cuerpo
        self.fila = fila
        self.columna = column

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        
        exp = self.exp.ejecutar(entorno)
        if(exp.tipo.esError()):
            TablaSimbolos.insertarError("Error en la expresion while: "+str(exp.getValor()),self.fila,self.columna)

        elif(exp.tipo.esBool()):
            TablaSimbolos.insertarCiclo('while')
            while(exp.getValor()):
                entorno.insertarEntorno('while')
                resCuerpo = self.cuerpo.ejecutar(entorno)
                entorno.eliminarEntorno()
                if(resCuerpo is not None):
                    if(resCuerpo.tipo.esBreak()):
                        if(TablaSimbolos.huboCiclo()):
                            entorno.eliminarEntorno()
                            TablaSimbolos.sacarCiclo()
                            return None
                        else:
                            TablaSimbolos.insertarError("Llamada continue fuera de un ciclo",self.fila,self.columna)
                            return None
                    elif(resCuerpo.tipo.esContinue()):
                        pass
                    elif(resCuerpo.tipo.esReturn()):
                        if(TablaSimbolos.huboLlamada()):
                            return resCuerpo
                        else:
                            TablaSimbolos.insertarError("Llamada return fuera de una funcion",self.fila,self.columna)
                            return None
                exp = self.exp.ejecutar(entorno)
        else:
            TablaSimbolos.insertarError("Error en el tipo de la expresion while: "+str(exp.tipo.getNombre()),self.fila,self.columna)

        return None

    def getArbol(self) -> str:
        nodo = Nodo("WHILE")
        nodo.addHoja(self.exp.getArbol())
        nodo.addHoja(self.cuerpo.getArbol())
        return nodo