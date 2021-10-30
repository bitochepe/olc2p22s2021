
from math import exp
from re import A
from typing import List
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.Primitivos.Tipo import Tipo

class Print(NodoAST):

    def __init__(self,fila:int,columna:int,exp:List[NodoAST],salto) -> None:
        self.fila = fila
        self.columna = columna
        self.exp = exp
        self.salto = salto

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        c3d = ""
        for x in self.exp:
            expRes = x.ejecutar(entorno)
            if(expRes.tipo.esBool()):
                etiqSalida = TablaSimbolos.getNewEtiq()
                c3d += expRes.getc3d()
                if(len(expRes.getEV())>0): c3d += expRes.getEV()+":"
                c3d += TablaSimbolos.printBoolean(1)
                c3d += "goto "+etiqSalida+";"
                if(len(expRes.getEF())>0): c3d += expRes.getEF()+":"
                c3d += TablaSimbolos.printBoolean(0)
                c3d += etiqSalida+":"

            elif(expRes.tipo.esFloat()):
                c3d += expRes.getc3d()
                c3d += "fmt.Printf(\"%f\", "+expRes.getValor()+");"

            elif(expRes.tipo.esChar()):
                c3d += expRes.getc3d()
                c3d += "fmt.Printf(\"%c\", "+expRes.getValor()+");"

            elif(expRes.tipo.esInt()):
                c3d += expRes.getc3d()
                c3d += "fmt.Printf(\"%d\", int("+expRes.getValor()+"));"

            elif(expRes.tipo.esString()):
                c3d += expRes.getc3d()
                t = TablaSimbolos.getNewTemp()
                t2 = TablaSimbolos.getNewTemp()
                codigo = t+" = p + 1;\n"+t2+" = stack[int("+t+")];\n"+"stack[int("+t+")] = "+expRes.getValor()+";\nprintString();\n"+"stack[int("+t+")] = "+t2+";"
                c3d += codigo

            elif(expRes.tipo.esBreak() or expRes.tipo.esContinue() or expRes.tipo.esNull()):
                #nuevo error semantico
                TablaSimbolos.insertarError("Sentencia break o continue dentro de print no admitida",self.fila,self.columna)

            elif(expRes.tipo.esReturn()):
                pass

            elif(expRes.tipo.esNull()):
                TablaSimbolos.insertarError("El valor de la variable es NUll",self.fila,self.columna)
            else:
                #error semantico
                TablaSimbolos.insertarError(expRes.getValor(),self.fila,self.columna)
                
        if(self.salto): c3d += "fmt.Printf(\"%c\", 10);\n"      
        return Primitivo("",Tipo(0),0,"","",c3d)

    def getArbol(self):
        nodo = Nodo("Print")
        for x in self.exp:
            nodo.addHoja(x.getArbol())
        return nodo