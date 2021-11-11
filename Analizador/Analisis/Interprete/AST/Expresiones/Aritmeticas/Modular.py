from math import prod
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Modular(NodoAST):

    def __init__(self, expDer:NodoAST, expIzq:NodoAST):
        self.expDer = expDer
        self.expIzq = expIzq

    def ejecutar(self, entorno):
        
        try:
            hizq = self.expIzq.ejecutar(entorno)
            hder = self.expDer.ejecutar(entorno)

            if(hizq.tipo.esError()): return hizq
            if(hder.tipo.esError()): return hder

            tipores = Tipo.getTipoResultado(hizq.tipo.getInt(),hder.tipo.getInt(),0)

            if(tipores == -1):
                return Primitivo("No es posible la operacion modular entre tipos: "+Tipo.getTipo(hizq.tipo.getInt())+" y "+Tipo.getTipo(hder.tipo.getInt()),Tipo(tipores),0,"","","")
            elif(tipores == 1):
                return self.generar(1,hizq,hder)
            elif(tipores == 2):
                return self.generar(2,hizq,hder)
            else:
                return Primitivo("Ocurrio un error desconocido",Tipo(-1),0,"","","")
        except Exception as e:
            return Primitivo(str(e),Tipo(-1),0,"","","")
    
    def getArbol(self):
        nodo = Nodo("Modular")
        nodo.addHoja(self.expIzq.getArbol())
        nodo.addHoja(Nodo("%"))
        nodo.addHoja(self.expDer.getArbol())
        return nodo

    def generar(self,tipo,i:Primitivo,d:Primitivo):
        op1 = TablaSimbolos.getNewTemp()
        op2 = TablaSimbolos.getNewTemp()
        l1 = TablaSimbolos.getNewEtiq() #si el divisor es 0
        l2 = TablaSimbolos.getNewEtiq() #salida del modular
        l3 = TablaSimbolos.getNewEtiq() #si el valor del divisor es negativo
        l4 = TablaSimbolos.getNewEtiq() #si el valor del numero es negativo
        l5 = TablaSimbolos.getNewEtiq() #etiqueta para el loop del modulo a mano
        l6 = TablaSimbolos.getNewEtiq() #etiqueta de salida del loop
        iterador = TablaSimbolos.getNewTemp()
        producto = TablaSimbolos.getNewTemp()

        tmp = TablaSimbolos.getNewTemp()
        c3d = i.getc3d() + "\n" + d.getc3d() + "\n"
        c3d += op1 + " = "+ i.getValor() + " + 0;\n"
        c3d += op2 + " = "+ d.getValor() + " + 0;\n"

        TablaSimbolos.temporalUsado(i.getValor())
        TablaSimbolos.temporalUsado(d.getValor())

        c3d += "if ("+op2+" != 0) {goto "+l1+";}\n"
        c3d +="fmt.Printf(\"%c\", 77);\n"
        c3d +="fmt.Printf(\"%c\", 97);\n"
        c3d +="fmt.Printf(\"%c\", 116);\n"
        c3d +="fmt.Printf(\"%c\", 104);\n"
        c3d +="fmt.Printf(\"%c\", 69);\n"
        c3d +="fmt.Printf(\"%c\", 114);\n"
        c3d +="fmt.Printf(\"%c\", 114);\n"
        c3d +="fmt.Printf(\"%c\", 111);\n"
        c3d +="fmt.Printf(\"%c\", 114);\n"
        c3d +=tmp +" = 0;\n"
        c3d +="goto "+l2+";\n"
        c3d +=l1+":\n"
        c3d += "if ("+op2+" > 0) {goto "+l3+";}\n"+op2+" = 0 - "+op2+";\n"+l3+":\n"
        c3d += "if ("+op1+" > 0) {goto "+l4+";}\n"+op1+" = 0 - "+op1+";\n"+l4+":\n"
        c3d += iterador +" = 1;\n"+producto+" = 0;\n"
        c3d += l5+":\n"
        c3d += "if ("+producto+" > "+op1+") {goto "+l6+";}\n"+producto+" = "+op2+" * "+iterador+";\n"+iterador+" = "+iterador+" + 1;\n"
        tmp2 = TablaSimbolos.getNewTemp()
        c3d += "goto "+l5+"\n"+l6+":\n"+ tmp2 + " = " + producto + " - " + op2 + ";\n"
        c3d += tmp + " = "+ op1 + " - "+ tmp2 + ";\n"
        c3d += l2+":\n"

        TablaSimbolos.temporalUsado(op1)
        TablaSimbolos.temporalUsado(op2)
        TablaSimbolos.temporalUsado(iterador)
        TablaSimbolos.temporalUsado(producto)
        TablaSimbolos.temporalUsado(tmp2)

        return Primitivo(tmp,Tipo(tipo),0,"","",c3d)