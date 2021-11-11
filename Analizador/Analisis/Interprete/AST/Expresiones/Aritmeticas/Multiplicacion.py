from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Multiplicacion(NodoAST):

    def __init__(self, expDer:NodoAST, expIzq:NodoAST):
        self.expDer = expDer
        self.expIzq = expIzq

    def ejecutar(self, entorno):
        
        try:
            hizq = self.expIzq.ejecutar(entorno)
            hder = self.expDer.ejecutar(entorno)

            if(hizq.tipo.esError()): return hizq
            if(hder.tipo.esError()): return hder

            tipores = Tipo.getTipoResultado(hizq.tipo.getInt(),hder.tipo.getInt(),1)

            if(tipores == -1):
                return Primitivo("No es posible multiplicar tipos: "+Tipo.getTipo(hizq.tipo.getInt())+" y "+Tipo.getTipo(hder.tipo.getInt()),Tipo(tipores),0,"","","")
            elif(tipores == 1):
                tmp = TablaSimbolos.getNewTemp()
                c3d = hizq.getc3d() + "\n" + hder.getc3d() +"\n"
                c3d += tmp+" = "+hizq.getValor()+" * "+hder.getValor()+";"
                TablaSimbolos.temporalUsado(hizq.getValor())
                TablaSimbolos.temporalUsado(hder.getValor())
                return Primitivo(tmp,Tipo(1),0,"","",c3d)
            elif(tipores == 2):
                tmp = TablaSimbolos.getNewTemp()
                c3d = hizq.getc3d() + "\n" + hder.getc3d() +"\n"
                c3d += tmp+" = "+hizq.getValor()+" * "+hder.getValor()+";"
                TablaSimbolos.temporalUsado(hizq.getValor())
                TablaSimbolos.temporalUsado(hder.getValor())
                return Primitivo(tmp,Tipo(2),0,"","",c3d)
            elif(tipores == 5):
                #operaciones con strings 3D
                return self.generar(hizq,hder)
            else:
                return Primitivo("Ocurrio un error desconocido",Tipo(-1),0,"","","")
        except Exception as e:
            return Primitivo(str(e),Tipo(-1),0,"","","")

    def getArbol(self):
        nodo = Nodo("Multiplicacion")
        nodo.addHoja(self.expIzq.getArbol())
        nodo.addHoja(Nodo("*"))
        nodo.addHoja(self.expDer.getArbol())
        return nodo

    def generar(self,hi:Primitivo,hd:Primitivo):
        t1 = TablaSimbolos.getNewTemp() #posicion heap cadena 1
        t2 = TablaSimbolos.getNewTemp() #posicion heap cadena 2
        t3 = TablaSimbolos.getNewTemp() #iterador
        t4 = TablaSimbolos.getNewTemp() #posicion heap cadena nueva
        etq = TablaSimbolos.getNewEtiq() #etiqueta inicio loop cadena 1
        etqs = TablaSimbolos.getNewEtiq() #etiqueta salida loop cadena 1
        etq2 = TablaSimbolos.getNewEtiq() #etiqueta inicio loop cadena 2
        etqs2 = TablaSimbolos.getNewEtiq() #etiqueta salida loop cadena 2

        c3d = hi.getc3d() +"\n"+ hd.getc3d()+"\n"
        c3d += t4+" = h + 0;\n"
        c3d += t1 + " = "+hi.getValor()+" + 0;\n"
        c3d += t2 + " = "+hd.getValor()+" + 0;\n"

        TablaSimbolos.temporalUsado(hi.getValor())
        TablaSimbolos.temporalUsado(hd.getValor())

        c3d += etq+":\n"+t3+" = heap[int("+t1+")];\n"
        c3d += "if "+t3+" == -234 {goto "+etqs+";}\nheap[int(h)] = "+t3+";\nh = h + 1;\n"
        c3d += t1+" = "+t1+" + 1;\ngoto "+etq+";\n"+etqs+":\n"

        c3d += etq2+":\n"+t3+" = heap[int("+t2+")];\n"
        c3d += "if "+t3+" == -234 {goto "+etqs2+";}\nheap[int(h)] = "+t3+";\nh = h + 1;\n"
        c3d += t2+" = "+t2+" + 1;\ngoto "+etq2+";\n"+etqs2+":\n"

        c3d += "heap[int(h)] = -234;\nh = h + 1;\n"

        TablaSimbolos.temporalUsado(t1)
        TablaSimbolos.temporalUsado(t2)
        TablaSimbolos.temporalUsado(t3)
        TablaSimbolos.temporalUsado(t4)

        return Primitivo(t4,Tipo(5),0,"","",c3d)