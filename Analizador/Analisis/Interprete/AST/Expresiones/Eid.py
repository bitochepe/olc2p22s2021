import re
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo


class Eid(NodoAST):

    def __init__(self,id,fila,columna):

        self.id = id
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno:TablaSimbolos):
        #buscar en el metodo de la ts el id y retoornar el valor
        v = entorno.getValor(self.id)
        if(v is not None):
             t1 = TablaSimbolos.getNewTemp()
             t2 = TablaSimbolos.getNewTemp()
             c3d = ""

             bajar = entorno.getPtrLess(self.id)
             if(bajar>0): 
                c3d += "p = p - "+str(bajar)+";\n"
                c3d += t1+" = p + "+str(v.getPos())+";\n"
                c3d += t2+" = stack[int("+t1+")];\n"
                c3d += "p = p + "+str(bajar)+";\n"
             else:   
                c3d += t1+" = p + "+str(v.getPos())+";\n"
                c3d += t2+" = stack[int("+t1+")];\n"
             vr = Primitivo(t2,v.getValor().tipo,0,v.getValor().getEV(),v.getValor().getEF(),c3d)
             return vr

        TablaSimbolos.insertarError("No existe la variable "+str(self.id),self.fila,self.columna)
        return Primitivo("No existe la variable "+str(self.id),Tipo(-1),0,"","","")
    
    def getArbol(self) -> str:
        nodo = Nodo("Primitivo")
        nodo.addHoja(Nodo("id: "+str(self.id)))
        return nodo
