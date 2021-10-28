from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.Primitivos.Tipo import Tipo

class For(NodoAST):

    def __init__(self, id:str,exp:NodoAST, cuerpo:Cuerpo, fila, column) -> None:
        self.id  =id
        self.exp = exp
        self.cuerpo = cuerpo
        self.fila = fila
        self.columna = column

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        
        exp = self.exp.ejecutar(entorno)
        if(exp.tipo.esError()):
            TablaSimbolos.insertarError("Error en la expresion For: "+str(exp.getValor()),self.fila,self.columna)

        elif(exp.tipo.getInt()== -2):#se itera un rango e in e
            limI = exp.getValor()[0]
            limS = exp.getValor()[1]
            entorno.insertarEntorno("iteradorFor")
            entorno.insertarVariable(self.id,Primitivo(limI,Tipo(1),0),1) #iterador
            TablaSimbolos.insertarCiclo('for')
            while(limI <= limS):
                entorno.insertarEntorno('cuerpoFor')
                resCuerpo = self.cuerpo.ejecutar(entorno)
                entorno.eliminarEntorno()
                if(resCuerpo is not None):
                    if(resCuerpo.tipo.esBreak()):
                        if(TablaSimbolos.huboCiclo()):
                            entorno.eliminarEntorno()
                            TablaSimbolos.sacarCiclo()
                            return None
                        else:
                            TablaSimbolos.insertarError("Llamada break fuera de un ciclo",self.fila,self.columna)
                            return None
                    elif(resCuerpo.tipo.esContinue()):
                        pass
                    elif(resCuerpo.tipo.esReturn()):
                        if(TablaSimbolos.huboLlamada()):
                            return resCuerpo
                        else:
                            TablaSimbolos.insertarError("Llamada return fuera de una funcion",self.fila,self.columna)
                limI = limI + 1
                entorno.setValor(self.id,Primitivo(limI,Tipo(1),0),1)
            entorno.eliminarEntorno()
            return None

        elif(exp.tipo.esString()): #Se itera un string
            entorno.insertarEntorno("iteradorFor")
            entorno.insertarVariable(self.id,Primitivo(0,Tipo(4),0),1)
            for x in exp.getValor():
                entorno.setValor(self.id,Primitivo(x,Tipo(4),0),Tipo(4))
                entorno.insertarEntorno("cuerpoFor")
                resCuerpo = self.cuerpo.ejecutar(entorno)
                entorno.eliminarEntorno()
                if(resCuerpo is not None):
                    if(resCuerpo.tipo.esBreak()):
                        if(TablaSimbolos.huboCiclo()):
                            entorno.eliminarEntorno()
                            TablaSimbolos.sacarCiclo()
                            return None
                        else:
                            TablaSimbolos.insertarError("Llamada break fuera de un ciclo",self.fila,self.columna)
                            return None
                    elif(resCuerpo.tipo.esContinue()):
                        pass
                    elif(resCuerpo.tipo.esReturn()):
                        if(TablaSimbolos.huboLlamada()):
                            return resCuerpo
                        else:
                            TablaSimbolos.insertarError("Llamada return fuera de una funcion",self.fila,self.columna)
                            return None
            entorno.eliminarEntorno()
            return None

        else:
            TablaSimbolos.insertarError("Error en el tipo de la expresion For: "+str(exp.tipo.getNombre()),self.fila,self.columna)

        return None

    def getArbol(self) -> str:
        nodo = Nodo("For")
        nodo.addHoja(self.exp.getArbol())
        nodo.addHoja(self.cuerpo.getArbol())
        return nodo