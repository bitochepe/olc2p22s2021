import re
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Relacional(NodoAST):

    def __init__(self, expDer:NodoAST, expIzq:NodoAST, op:int):
        self.expDer = expDer
        self.expIzq = expIzq
        self.op = op

    def ejecutar(self, entorno):
        
        try:
            hizq = self.expIzq.ejecutar(entorno)
            hder = self.expDer.ejecutar(entorno)

            if(hizq.tipo.esError()): return hizq
            if(hder.tipo.esError()): return hder

            tipores = Tipo.getTipoResultado(hizq.tipo.getInt(),hder.tipo.getInt(),3)

            if(tipores == -1):
                return Primitivo("No es posible la operacion relacional entre tipos: "+Tipo.getTipo(hizq.tipo.getInt())+" y "+Tipo.getTipo(hder.tipo.getInt()),Tipo(-1),0,"","","")
            elif(tipores == 3):
                # 0:> 1:< 2:>= 3:<= 4:== 5:!=
                if(hizq.tipo.esString() and hder.tipo.esString()):
                    if(self.op == 0):
                        return self.generarSTR(hizq,hder," > ")
                    elif(self.op == 1):
                        return self.generarSTR(hizq,hder," < ")
                    elif(self.op == 2):
                        return self.generarSTR(hizq,hder," >= ")
                    elif(self.op == 3):
                        return self.generarSTR(hizq,hder," <= ")
                    elif(self.op == 4):
                        return self.generarSTR(hizq,hder," == ")
                    elif(self.op == 5):
                        return self.generarSTR(hizq,hder," != ")
                    pass
                else:
                    if(self.op == 0):
                        return self.generar(hizq,hder," > ")
                    elif(self.op == 1):
                        return self.generar(hizq,hder," < ")
                    elif(self.op == 2):
                        return self.generar(hizq,hder," >= ")
                    elif(self.op == 3):
                        return self.generar(hizq,hder," <= ")
                    elif(self.op == 4):
                        return self.generar(hizq,hder," == ")
                    elif(self.op == 5):
                        return self.generar(hizq,hder," != ")
            else:
                return Primitivo("Ocurrio un error desconocido",Tipo(-1),0,"","")
        except Exception as e:
            return Primitivo(str(e),Tipo(-1),0,"","","")
    
    def getArbol(self):
        #0:> 1:< 2:>= 3:<= 4:== 5:!=
        nodo = Nodo("Relacional")
        nodo.addHoja(self.expIzq.getArbol())
        if(self.op == 0):
            nodo.addHoja(Nodo(">"))
        elif(self.op == 1):
            nodo.addHoja(Nodo("<"))
        elif(self.op == 2):
            nodo.addHoja(Nodo(">="))
        elif(self.op == 3):
            nodo.addHoja(Nodo("<="))
        elif(self.op == 4):
            nodo.addHoja(Nodo("=="))
        elif(self.op == 5):
            nodo.addHoja(Nodo("!="))
        else:
            nodo.addHoja(Nodo(""))
        nodo.addHoja(self.expDer.getArbol())
        return nodo

    def generar(self,i:Primitivo,d:Primitivo,o):
        EtiqV = TablaSimbolos.getNewEtiq()
        EtiqF = TablaSimbolos.getNewEtiq()
        c3d = i.getc3d() +"\n" + d.getc3d() +"\n"
        c3d += "if "+i.getValor()+o+d.getValor()+" {goto "+EtiqV+";}\ngoto "+EtiqF+";"

        TablaSimbolos.temporalUsado(i.getValor())
        TablaSimbolos.temporalUsado(d.getValor())

        return Primitivo("0",Tipo(3),0,EtiqV,EtiqF,c3d)

    def generarSTR(self,i:Primitivo,d:Primitivo):
        pass