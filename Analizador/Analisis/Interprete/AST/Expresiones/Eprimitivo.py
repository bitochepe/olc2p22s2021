from math import e
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.Primitivos.Tipo import Tipo

class Eprimitivo(NodoAST):

    def __init__(self,valor,tipo:Tipo,dimension):
        self.valor = valor
        self.tipo = tipo
        self.dimension = dimension

    def ejecutar(self, entorno):
        if(self.tipo.esBool()):
            etiq = TablaSimbolos.getNewEtiq()
            if(self.valor == 1):
                return Primitivo("1",self.tipo,self.dimension,etiq,"","goto "+etiq+";")
            else:
                return Primitivo("0",self.tipo,self.dimension,"",etiq,"goto "+etiq+";")
        elif(self.tipo.esString()):
            t = TablaSimbolos.getNewTemp()
            c3d = t+" = h + 0;\n"
            for caracter in self.valor: 
                c3d += "heap[int(h)] = "+str(ord(caracter))+";\n"
                c3d += "h = h + 1;\n"
            c3d += "heap[int(h)] = -234;\n"
            c3d += "h = h + 1;\n"
            return Primitivo(t,self.tipo,self.dimension,"","",c3d)
        return Primitivo(str(self.valor),self.tipo,self.dimension,"","","")

    def getArbol(self):
        nodo = Nodo("Primitivo")
        nodo.addHoja(Nodo(self.valor))
        return nodo


