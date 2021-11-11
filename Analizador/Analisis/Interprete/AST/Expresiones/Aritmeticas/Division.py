from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Division(NodoAST):

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
                return Primitivo("No es posible dividir tipos: "+Tipo.getTipo(hizq.tipo.getInt())+" y "+Tipo.getTipo(hder.tipo.getInt()),Tipo(tipores),0,"","","")
            elif(tipores == 1):
                return self.generar(1,hizq,hder)

            elif(tipores == 2):
                return self.generar(2,hizq,hder)
            else:
                return Primitivo("Ocurrio un error desconocido",Tipo(-1),0,"","","")
        except Exception as e:
            return Primitivo(str(e),Tipo(-1),0,"","","")

    def getArbol(self):
        nodo = Nodo("Division")
        nodo.addHoja(self.expIzq.getArbol())
        nodo.addHoja(Nodo("/"))
        nodo.addHoja(self.expDer.getArbol())
        return nodo
    
    def generar(self,tipo,i:Primitivo,d:Primitivo):
        l1 = TablaSimbolos.getNewEtiq()
        l2 = TablaSimbolos.getNewEtiq()
        tmp = TablaSimbolos.getNewTemp()
        c3d = i.getc3d() +"\n"+ d.getc3d() +"\n"
        c3d += "if ("+d.getValor()+" != 0) {goto "+l1+";}\n"
        c3d +="fmt.Printf(\"%c\", 77);\n"
        c3d +="fmt.Printf(\"%c\", 97);\n"
        c3d +="fmt.Printf(\"%c\", 116);\n"
        c3d +="fmt.Printf(\"%c\", 104);\n"
        c3d +="fmt.Printf(\"%c\", 69);\n"
        c3d +="fmt.Printf(\"%c\", 114);\n"
        c3d +="fmt.Printf(\"%c\", 114);\n"
        c3d +="fmt.Printf(\"%c\", 111);\n"
        c3d +="fmt.Printf(\"%c\", 114);\n"
        c3d +=tmp+" = 0;\n"
        c3d +="goto "+l2+";\n"
        c3d +=l1+":\n"
        c3d += tmp + " = " + i.getValor() + " / " + d.getValor() +";\n"
        c3d += l2+":\n"

        TablaSimbolos.temporalUsado(i.getValor())
        TablaSimbolos.temporalUsado(d.getValor())

        return Primitivo(tmp,Tipo(tipo),0,"","",c3d)