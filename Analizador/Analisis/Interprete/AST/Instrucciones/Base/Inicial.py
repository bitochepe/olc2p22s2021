from math import tan
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.AST.Instrucciones.Base.NodoFuncion import NodoFuncion
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.AST.Instrucciones.Nativas.Nativas import Nativas
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Expresiones.Eid import Eid

class Inicial(NodoAST):

    def __init__(self) -> None:
        pass

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        funciones = ""
        #NodoFuncion('log10',['$x'],Cuerpo([Nativas(Eid("$x",1,1),None,1,1,1)])).ejecutar(entorno)
        #NodoFuncion('log',['$x','$base'],Cuerpo([Nativas(Eid('$x',1,1),Eid('$base',1,1),2,1,1)])).ejecutar(entorno)
        #NodoFuncion('sin',['$x'],Cuerpo([Nativas(Eid('$x',1,1),None,3,1,1)])).ejecutar(entorno)
        #NodoFuncion('cos',['$x'],Cuerpo([Nativas(Eid('$x',1,1),None,4,1,1)])).ejecutar(entorno)
        #NodoFuncion('tan',['$x'],Cuerpo([Nativas(Eid('$x',1,1),None,5,1,1)])).ejecutar(entorno)
        #NodoFuncion('sqrt',['$x'],Cuerpo([Nativas(Eid('$x',1,1),None,6,1,1)])).ejecutar(entorno)
        funciones += self.generarPrintString()
        return funciones

    def getArbol(self) -> str:
        pass

    def generarPrintString(self):
        t1 = TablaSimbolos.getNewTemp()
        t2 = TablaSimbolos.getNewTemp()
        t3 = TablaSimbolos.getNewTemp()
        etq = TablaSimbolos.getNewEtiq()
        etqs = TablaSimbolos.getNewEtiq()

        codigo = "func printString(){\n"
        codigo += t1 +" = "+"p + 1;\n"+t2+" = "+"stack[int("+t1+")];\n"
        codigo += etq+":\n"+t3+" = heap[int("+t2+")];\n"
        codigo += "if "+t3+" == -234 {goto "+etqs+";}\nfmt.Printf(\"%c\",int("+t3+"));\n"
        codigo += t2+" = "+t2+" + 1;\ngoto "+etq+";\n"+etqs+":\nreturn;\n}\n"
        return codigo
