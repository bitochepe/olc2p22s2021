from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Nodo import Nodo
import math

class Nativas(NodoAST):

    def __init__(self,exp:NodoAST,exp2:NodoAST,num:int,fila,columna) -> None:
        #num: 1: log10()  2: log()  3: sin()  4 : cos()     5 : tan()   6: sqrt()
        #num: 7: uppercase
        self.num = num
        self.exp = exp
        self.exp2 = exp2
        self.fila = fila    
        self.columna = columna

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        
        resExp = self.exp.ejecutar(entorno)
        if(resExp.tipo.esError()):
            return Primitivo(resExp.getValor(),Tipo(-1),0,"","")

        if(self.num == 1):
            if(resExp.tipo.esInt() or resExp.tipo.esFloat()):
                return Primitivo(math.log10(resExp.getValor()),Tipo(2),0,"","")
            else:
                return Primitivo("Tipo invalido para funcion log10: "+resExp.tipo.getNombre(),Tipo(-1),0,"","")

        elif(self.num == 2):
            if(resExp.tipo.esInt() or resExp.tipo.esFloat()):
                if(self.exp2 is not None):
                    resExp2 = self.exp2.ejecutar(entorno)
                    if(resExp2.tipo.esInt() or resExp2.tipo.esFloat()):
                        return Primitivo(math.log(resExp2.getValor(),resExp.getValor()),Tipo(2),0,"","")
                    else:
                        return Primitivo("Tipo invalido en base para funcion log: "+resExp2.tipo.getNombre(),Tipo(-1),0,"","")
                else:
                    return Primitivo(math.log(resExp.getValor()),Tipo(2),0,"","")
            else:
                return Primitivo("Tipo invalido para funcion log: "+resExp.tipo.getNombre(),Tipo(-1),0,"","")
                
        elif(self.num == 3):
            if(resExp.tipo.esInt() or resExp.tipo.esFloat()):
                return Primitivo(math.sin(resExp.getValor()),Tipo(2),0,"","")
            else:
                return Primitivo("Tipo invalido para funcion sin: "+resExp.tipo.getNombre(),Tipo(-1),0,"","")
        elif(self.num == 4):
            if(resExp.tipo.esInt() or resExp.tipo.esFloat()):
                return Primitivo(math.cos(resExp.getValor()),Tipo(2),0,"","")
            else:
                return Primitivo("Tipo invalido para funcion cos: "+resExp.tipo.getNombre(),Tipo(-1),0,"","")
        elif(self.num == 5):
            if(resExp.tipo.esInt() or resExp.tipo.esFloat()):
                return Primitivo(math.tan(resExp.getValor()),Tipo(2),0,"","")
            else:
                return Primitivo("Tipo invalido para funcion tan: "+resExp.tipo.getNombre(),Tipo(-1),0,"","")
        elif(self.num == 6):
            if(resExp.tipo.esInt() or resExp.tipo.esFloat()):
                return Primitivo(math.sqrt(resExp.getValor()),Tipo(2),0,"","")
            else:
                return Primitivo("Tipo invalido para funcion sqrt: "+resExp.tipo.getNombre(),Tipo(-1),0,"","")
        else:
            return Primitivo("Funcion no definida",Tipo(-1),0,"","")
        

    def getArbol(self) -> str:
        if(self.num == 1):
            return Nodo("log10")
        elif(self.num == 1):
            return Nodo("log")
        elif(self.num == 1):
            return Nodo("sin")
        elif(self.num == 1):
            return Nodo("cos")
        elif(self.num == 1):
            return Nodo("tan")
        elif(self.num == 1):
            return Nodo("sqrt")
        else:
            return Nodo("Error")
        
        
