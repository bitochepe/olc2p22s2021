
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.Primitivos.Tipo import Tipo

class If(NodoAST):

    def __init__(self,cuerpoIF:NodoAST,cuerpoElse:NodoAST,exp:NodoAST,fila:int,columna:int) -> None:
        self.cuerpoIF = cuerpoIF
        self.cuerpoElse = cuerpoElse
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno) -> Primitivo:
        Rexp = self.exp.ejecutar(entorno)
        if(Rexp.tipo.esError()):
            TablaSimbolos.insertarError(Rexp.valor,self.fila,self.columna)
            return None
        
        elif(Rexp.tipo.esBool()):
            Lsalida = TablaSimbolos.getNewEtiq()
            c3d = Rexp.getc3d() +"\n"
            c3d += Rexp.getEV() +":\n"

            if(self.cuerpoIF is not None): 
                cif = self.cuerpoIF.ejecutar(entorno)
                c3d += cif.getc3d() + "\n"
                
                if(cif.tipo.esReturn()):
                    pass
                elif(cif.tipo.esBreak()):
                    pass
                elif(cif.tipo.esContinue()):
                    pass
            c3d += "goto "+Lsalida+";\n"
            c3d += Rexp.getEF() +":\n"
            if(self.cuerpoElse is not None): 
                celse = self.cuerpoElse.ejecutar(entorno)
                c3d += celse.getc3d() + "\n"
                
                if(cif.tipo.esReturn()):
                    pass
                elif(cif.tipo.esBreak()):
                    pass
                elif(cif.tipo.esContinue()):
                    pass
            c3d += Lsalida+":\n"
            
            return Primitivo("",Tipo(0),0,"","",c3d)

            # if(Rexp.valor):
            #     resCuerpo = self.cuerpoIF.ejecutar(entorno)
            #     if(resCuerpo is not None):
            #         if(resCuerpo.tipo.esBreak()):
            #             return resCuerpo
            #         elif(resCuerpo.tipo.esContinue()):
            #             return resCuerpo
            #         elif(resCuerpo.tipo.esReturn()):
            #             return resCuerpo
            # else:
            #     if(Rexp.valor!=None):
            #         if(self.cuerpoElse is not None):
            #             resCuerpo = self.cuerpoElse.ejecutar(entorno)
            #             if(resCuerpo is not None):
            #                 if(resCuerpo.tipo.esBreak()):
            #                     return resCuerpo
            #                 elif(resCuerpo.tipo.esContinue()):
            #                     return resCuerpo
            #                 elif(resCuerpo.tipo.esReturn()):
            #                     return resCuerpo
            #     return None
        else:
            TablaSimbolos.insertarError("Tipo de expresion invalido: \""+Rexp.tipo.getTipo()+"\"",self.fila,self.columna)
            return None
    

    def getArbol(self) -> str:
        nodo = Nodo("If")
        nodo.addHoja(Nodo("if"))
        nodo.addHoja(self.exp.getArbol())
        nodo.addHoja(self.cuerpoIF.getArbol())

        if(self.cuerpoElse is not None):
            nodo.addHoja(Nodo("else"))
            nodo.addHoja(self.cuerpoElse.getArbol())

        return nodo