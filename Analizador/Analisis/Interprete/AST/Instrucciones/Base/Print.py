
from math import exp
from re import A
from typing import List
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Nodo import Nodo

class Print(NodoAST):

    def __init__(self,fila:int,columna:int,exp:List[NodoAST],salto) -> None:
        self.fila = fila
        self.columna = columna
        self.exp = exp
        self.salto = salto

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        for x in self.exp:
            expRes = x.ejecutar(entorno)
            if(expRes.tipo.esBool()):
                etiqSalida = TablaSimbolos.getNewEtiq()
                TablaSimbolos.insertarSalida(expRes.getc3d())
                if(len(expRes.getEV())>0): TablaSimbolos.insertarSalida(expRes.getEV()+":")
                TablaSimbolos.printBoolean(1)
                TablaSimbolos.insertarSalida("goto "+etiqSalida+";")
                if(len(expRes.getEF())>0): TablaSimbolos.insertarSalida(expRes.getEF()+":")
                TablaSimbolos.printBoolean(0)
                TablaSimbolos.insertarSalida(etiqSalida+":")

            elif(expRes.tipo.esFloat()):
                TablaSimbolos.insertarSalida(expRes.getc3d())
                TablaSimbolos.insertarSalida("fmt.Printf(\"%f\", "+expRes.getValor()+");")

            elif(expRes.tipo.esChar()):
                TablaSimbolos.insertarSalida(expRes.getc3d())
                TablaSimbolos.insertarSalida("fmt.Printf(\"%c\", "+expRes.getValor()+");")

            elif(expRes.tipo.esInt()):
                TablaSimbolos.insertarSalida(expRes.getc3d())
                TablaSimbolos.insertarSalida("fmt.Printf(\"%d\", int("+expRes.getValor()+"));")

            elif(expRes.tipo.esString()):
                TablaSimbolos.insertarSalida(expRes.getc3d())
                t = TablaSimbolos.getNewTemp()
                t2 = TablaSimbolos.getNewTemp()
                codigo = t+" = p + 1;\n"+t2+" = stack[int("+t+")];\n"+"stack[int("+t+")] = "+expRes.getValor()+";\nprintString();\n"+"stack[int("+t+")] = "+t2
                TablaSimbolos.insertarSalida(codigo)

            elif(expRes.tipo.esBreak() or expRes.tipo.esContinue() or expRes.tipo.esNull()):
                #nuevo error semantico
                TablaSimbolos.insertarError("Sentencia break o continue dentro de print no admitida",self.fila,self.columna)
    
            elif(expRes.tipo.esReturn()):
                TablaSimbolos.insertarSalida(expRes.getc3d())
                TablaSimbolos.insertarSalida(str(expRes.getValor().getValor()))

            elif(expRes.tipo.esNull()):
                TablaSimbolos.insertarError("El valor de la variable es NUll",self.fila,self.columna)
            else:
                #error semantico
                TablaSimbolos.insertarError(expRes.getValor(),self.fila,self.columna)
                
        if(self.salto):TablaSimbolos.insertarSalida("fmt.Printf(\"%c\", 10);\n")         
        return None

    def getArbol(self):
        nodo = Nodo("Print")
        for x in self.exp:
            nodo.addHoja(x.getArbol())
        return nodo