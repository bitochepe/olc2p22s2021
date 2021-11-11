from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Potencia(NodoAST):

    def __init__(self, expDer:NodoAST, expIzq:NodoAST):
        self.expDer = expDer
        self.expIzq = expIzq

    def ejecutar(self, entorno):
        
        try:
            hizq = self.expIzq.ejecutar(entorno)
            hder = self.expDer.ejecutar(entorno)

            if(hizq.tipo.esError()): return hizq
            if(hder.tipo.esError()): return hder

            tipores = Tipo.getTipoResultado(hizq.tipo.getInt(),hder.tipo.getInt(),2)

            if(tipores == -1):
                return Primitivo("No es posible la operacion potencia entre tipos: "+Tipo.getTipo(hizq.tipo.getInt())+" y "+Tipo.getTipo(hder.tipo.getInt()),Tipo(-1),0,"","","")
            elif(tipores == 1):
                return self.generar(hizq,hder,1)
            elif(tipores == 2):
                return self.generar(hizq,hder,2)
            elif(tipores == 5):
                return self.generarSTR(hizq,hder)
            else:
                return Primitivo("Ocurrio un error desconocido",Tipo(-1),0,"","","")
        except Exception as e:
            return Primitivo(str(e),Tipo(-1),0,"","","")
    
    def getArbol(self):
        nodo = Nodo("Potencia")
        nodo.addHoja(self.expIzq.getArbol())
        nodo.addHoja(Nodo("^"))
        nodo.addHoja(self.expDer.getArbol())
        return nodo

    def generar(self,i:Primitivo,d:Primitivo,t:int):
        op1 = TablaSimbolos.getNewTemp()
        op2 = TablaSimbolos.getNewTemp()
        aux = TablaSimbolos.getNewTemp() #temporal que guarda una copia del exponente
        c3d = i.getc3d() + "\n" + i.getc3d() +"\n"
        c3d += op1 + " = "+ i.getValor() + " + 0;\n"
        c3d += op2 + " = "+ d.getValor() + " + 0;\n"
        c3d += aux + " = "+ i.getValor() + " + 0;\n"
        et1 = TablaSimbolos.getNewEtiq() #etiqueta para potencias 0
        et2 = TablaSimbolos.getNewEtiq() #etiqueta para potencias negativas
        et3 = TablaSimbolos.getNewEtiq() #etiqueta de salida

        TablaSimbolos.temporalUsado(i.getValor())
        TablaSimbolos.temporalUsado(d.getValor())

        c3d += "if "+op2+" == 0 {goto "+et1+";} \nif "+op2+" < 0 {goto "+et2+";}\n" 
        c3d += op2 + " = " + op2 +" - 1;\n"

        #ciclo para potencia positiva
        sl = TablaSimbolos.getNewEtiq()
        c3d += sl +":\nif "+op2+" <= 0 {goto "+et3+";}\n"+op1+" = "+op1+" * "+aux+";\n"+op2+" = "+op2+" - 1;\ngoto "+sl+";\n"
        
        #ciclo para potencia 0
        c3d += et1 +":\n"+op1+" = 1;\ngoto "+et3+";\n"

        #ciclo para potencias negativas
        sl = TablaSimbolos.getNewEtiq()
        sl2 = TablaSimbolos.getNewEtiq()
        c3d += et2 +":\n"+op2+" = "+op2+" + 1;\n"+sl+":\nif "+op2+" >= 0 {goto "+sl2+";}\n"+op1+" = "+op1+" * "+aux+";\n"+op2+" = "+op2+" + 1;\ngoto "+sl+";\n"+sl2+":\n"+op1+" = 1 / "+op1+";\ngoto "+et3+";\n"+et3+":"

        TablaSimbolos.temporalUsado(op2)
        TablaSimbolos.temporalUsado(aux)

        return Primitivo(op1,Tipo(t),0,"","",c3d)

    def generarSTR(self,hi:Primitivo,hd:Primitivo):
        t0 = TablaSimbolos.getNewTemp() #posicion heap nueva cadena
        t1 = TablaSimbolos.getNewTemp() #posicion heap cadena
        t3 = TablaSimbolos.getNewTemp() #iterador del heap
        t4 = TablaSimbolos.getNewTemp() #iterador del loop
        etq = TablaSimbolos.getNewEtiq() #inicio loop
        etqs = TablaSimbolos.getNewEtiq() #salida loop

        c3d = hi.getc3d() +"\n"+ hd.getc3d() +"\n"
        c3d += t0 + " = h + 0;\n"
        c3d += t1 + " = "+hi.getValor()+"\n"
        c3d += t4+ " = "+hd.getValor()+" + 0;\n"
        c3d += etq+":\n"+t3+" = heap[int("+t1+")];\n"
        c3d += "if "+t3+" == -234 {goto "+etqs+";}\nheap[int(h)] = "+t3+";\nh = h + 1;\n"
        c3d += t1+" = "+t1+" + 1;\ngoto "+etq+";\n"+etqs+":\n"
        c3d += t4 + " = "+t4+" - 1;\nif("+t4+" > 0){\n"
        c3d += t1 + " = "+hi.getValor()+"\ngoto "+etq+";\n}\n"
        c3d += "heap[int(h)] = -234;\nh = h + 1;\n"

        TablaSimbolos.temporalUsado(t1)
        TablaSimbolos.temporalUsado(t3)
        TablaSimbolos.temporalUsado(t4)
        TablaSimbolos.temporalUsado(hi.getValor())
        TablaSimbolos.temporalUsado(hd.getValor())

        return Primitivo(t0,Tipo(5),0,"","",c3d)