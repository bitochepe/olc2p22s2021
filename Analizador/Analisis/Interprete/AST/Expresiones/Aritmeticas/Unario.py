from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Unario(NodoAST):

    def __init__(self, exp:NodoAST,signo:bool):
        self.exp = exp
        self.signo = signo

    def ejecutar(self, entorno):
        
        try:
            ex = self.exp.ejecutar(entorno)

            if(ex.tipo.esError()): return ex

            if(ex.tipo.esInt()):
                if(self.signo):
                    tmp = TablaSimbolos.getNewTemp()
                    c3d = ex.getc3d() + "\n" 
                    c3d +=tmp+" = 0 + "+ex.getValor()+";"
                    TablaSimbolos.temporalUsado(ex.getValor())
                    return Primitivo(tmp,Tipo(1),0,"","",c3d)
                else:
                    tmp = TablaSimbolos.getNewTemp()
                    c3d = ex.getc3d() + "\n"
                    c3d += tmp+" = 0 - "+ex.getValor()+";"
                    TablaSimbolos.temporalUsado(ex.getValor())
                    return Primitivo(tmp,Tipo(1),0,"","",c3d)
            
            elif(ex.tipo.esFloat()):
                if(self.signo):
                    tmp = TablaSimbolos.getNewTemp()
                    c3d = ex.getc3d() + "\n"
                    c3d += tmp+" = 0 + "+ex.getValor()+";"
                    TablaSimbolos.temporalUsado(ex.getValor())
                    return Primitivo(tmp,Tipo(2),0,"","",c3d)
                else:
                    tmp = TablaSimbolos.getNewTemp()
                    c3d = ex.getc3d() + "\n"
                    c3d += tmp+" = 0 - "+ex.getValor()+";"
                    TablaSimbolos.temporalUsado(ex.getValor())
                    return Primitivo(tmp,Tipo(2),0,"","",c3d)
            else:
                return Primitivo("Error de tipo unario: "+ex.tipo.getTipo(),Tipo(-1),0,"","","")

        except Exception as e:
            return Primitivo(str(e),Tipo(-1),0,"","","")

    def getArbol(self):
        nodo = Nodo("Unario")
        if(self.signo):
            nodo.addHoja(Nodo("+"))
        else:
            nodo.addHoja(Nodo("-"))
        nodo.addHoja(self.exp.getArbol())
        return nodo