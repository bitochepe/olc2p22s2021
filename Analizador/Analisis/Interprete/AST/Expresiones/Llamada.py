
from typing import List
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.Nodo import Nodo

class Llamada(NodoAST):

    def __init__(self,id,parametros:List[NodoAST],fila,columna) -> None:
        self.id = id
        self.parametros = parametros
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        
        funcion = entorno.existeFuncion(self.id)
        if(funcion is not None):
            if(len(self.parametros) == len(funcion.parametros)):
                entorno.insertarEntorno('funcion'+self.id)
                try:
                    it = 0
                    for x in self.parametros:
                        auxE = entorno.eliminarEntorno()
                        aux = x.ejecutar(entorno)
                        if(aux.tipo.esError()):
                            return Primitivo("Error en parametros funcion "+str(self.id),Tipo(-1),0,"","")
                        else:
                            entorno.insertarEntornoE(auxE)
                            entorno.insertarVariable(funcion.parametros[it],aux,0)
                            it = it + 1
                    resCuerpo = funcion.cuerpo.ejecutar(entorno)
                    if(resCuerpo is not None):
                        if(resCuerpo.tipo.esReturn()):
                            return resCuerpo.getValor()
                    return None
                except:
                    return Primitivo('Error en servidor al correr funcion',Tipo(-1),0,"","")
            else:
                return Primitivo("Parametros mal definido para la funcion \""+str(self.id)+"\"",Tipo(-1),0,"","")
        else:
            return Primitivo("Funcion \""+str(self.id)+"\" no definida",Tipo(-1),0,"","")

    def getArbol(self) -> str:
        nodo = Nodo("Llamada")
        nodo.addHoja(Nodo(self.id))
        return nodo


