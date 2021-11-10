from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Logica(NodoAST):

    def __init__(self, expDer:NodoAST, expIzq:NodoAST, op:int):
        self.expDer = expDer
        self.expIzq = expIzq
        self.op = op

    def ejecutar(self, entorno):
        
        try:
            hizq = self.expIzq.ejecutar(entorno)
            if(self.expDer is None):                
                if(hizq.tipo.esError()): return hizq
                if(hizq.tipo.getInt()):
                    if(self.op == 2):
                        return Primitivo("0",Tipo(3),0,hizq.getEF(),hizq.getEV(),hizq.getc3d())
                    else:
                        return Primitivo("Ocurrio un error desconocido",Tipo(-1),0,"","","")
            else:
                hder = self.expDer.ejecutar(entorno)
                if(hizq.tipo.esError()): return hizq
                if(hder.tipo.esError()): return hder

                tipores = Tipo.getTipoResultado(hizq.tipo.getInt(),hder.tipo.getInt(),4)

                if(tipores == -1):
                    return Primitivo("No es posible la operacion logica entre tipos: "+Tipo.getTipo(hizq.tipo.getInt())+" y "+Tipo.getTipo(hder.tipo.getInt()),Tipo(-1),0,"","","")
                elif(tipores == 3):
                    # 0:|| 1:&& 2:! 
                    if(self.op == 0):
                        etiqV = ""
                        if(len(hizq.getEV())>0 and len(hder.getEV())>0): 
                            etiqV += hizq.getEV() +": "+ hder.getEV()
                        else:
                            etiqV += hizq.getEV() + hder.getEV()
                        etiqF = hder.getEF()

                        c3d = hizq.getc3d()+"\n"
                        if(len(hizq.getEF())>0): c3d+=hizq.getEF()+":\n"
                        c3d += hder.getc3d()
                        return Primitivo("0",Tipo(3),0,etiqV,etiqF,c3d)

                    elif(self.op == 1):
                        etiqF = ""
                        if(len(hizq.getEF())>0 and len(hder.getEF())>0): 
                            etiqF += hizq.getEF() +": "+ hder.getEF()
                        else:
                            etiqF += hizq.getEF() + hder.getEF()
                        etiqV = hder.getEV()

                        c3d = hizq.getc3d()+"\n"
                        if(len(hizq.getEV())>0): c3d+=hizq.getEV()+":\n"
                        c3d += hder.getc3d()
                        return Primitivo("0",Tipo(3),0,etiqV,etiqF,c3d)
                else:
                    return Primitivo("Ocurrio un error desconocido",Tipo(-1),0,"","")
        except Exception as e:
            return Primitivo(str(e),Tipo(-1),0,"","","")

    def getArbol(self):
        nodo = Nodo("Logica")
        nodo.addHoja(self.expIzq.getArbol())
        if(self.op == 0):
            nodo.addHoja(Nodo("OR"))
        elif(self.op == 1):
            nodo.addHoja(Nodo("AND"))
        elif(self.op == 2):
            nodo.addHoja(Nodo("NOT"))
        else:
            nodo.addHoja(Nodo(""))
        nodo.addHoja(self.expDer.getArbol())
        return nodo