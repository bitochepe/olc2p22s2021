from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Suma(NodoAST):

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
                return Primitivo("No es posible sumar tipos: "+Tipo.getTipo(hizq.tipo.getInt())+" y "+Tipo.getTipo(hder.tipo.getInt()),Tipo(-1),0,"","","")
            elif(tipores == 1):
                tmp = TablaSimbolos.getNewTemp()
                c3d = hizq.getc3d() + "\n" + hder.getc3d() +"\n"
                c3d +=tmp+" = "+hizq.getValor()+" + "+hder.getValor()+";"
                TablaSimbolos.temporalUsado(hizq.getValor())
                TablaSimbolos.temporalUsado(hder.getValor())
                return Primitivo(tmp,Tipo(1),0,"","",c3d)
            elif(tipores == 2):
                tmp = TablaSimbolos.getNewTemp()
                c3d = hizq.getc3d() + "\n" + hder.getc3d() +"\n"
                c3d += tmp+" = "+hizq.getValor()+" + "+hder.getValor()+";"
                TablaSimbolos.temporalUsado(hizq.getValor())
                TablaSimbolos.temporalUsado(hder.getValor())
                return Primitivo(tmp,Tipo(2),0,"","",c3d)
            else:
                return Primitivo("Ocurrio un error desconocido",Tipo(-1),0,"","","")
        except Exception as e:
            return Primitivo(str(e),Tipo(-1),0,"","","")

    def getArbol(self):
        nodo = Nodo("Suma")
        nodo.addHoja(self.expIzq.getArbol())
        nodo.addHoja(Nodo("+"))
        nodo.addHoja(self.expDer.getArbol())
        return nodo