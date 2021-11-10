
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.Nodo import Nodo

class Return(NodoAST):

    def __init__(self,exp:NodoAST,fila,columna) -> None:
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        c3d = "return;\n"
        if(self.exp is not None):
            resExp = self.exp.ejecutar(entorno)
            if(resExp.tipo.esError()):
                TablaSimbolos.insertarError("Error en sentencia Return: "+str(resExp.getValor()),self.fila,self.columna)
                return Primitivo("",Tipo(0),0,"","","")

            if(TablaSimbolos.huboLlamada()):
                
                bajar = entorno.getPtrLess("$retorno$")
                t1 = TablaSimbolos.getNewTemp()
                if(bajar>0): 
                    entorno.setValor("$retorno$",resExp,0)
                    entorno.setValor("$tipo$",resExp,0)
                    v = entorno.getValor("$retorno$")
                    
                    if(resExp.tipo.esBool()):
                        c3d = resExp.getc3d()+";\n"
                        if(len(resExp.getEV())>0):c3d+=resExp.getEV()+":"
                        if(len(resExp.getEF())>0):c3d+=resExp.getEF()+":"
                        c3d+="\n"
                    else:
                        c3d = resExp.getc3d()+";\n"
                    c3d += "p = p - "+str(bajar)+";\n"
                    c3d += t1+" = p + "+str(v.getPos())+";\n"
                    c3d += "stack[int("+t1+")] = "+resExp.getValor()+";\n"    
                    c3d += t1+" = p + "+str(v.getPos()+1)+";\n"
                    c3d += "stack[int("+t1+")] = "+str(resExp.tipo.getInt())+";\n"
                    c3d += "p = p + "+str(bajar)+";\n"
                    c3d += "return;\n"
                else:   
                    entorno.setValor("$retorno$",resExp,0)
                    entorno.setValor("$tipo$",resExp,0)
                    v = entorno.getValor("$retorno$")

                    if(resExp.tipo.esBool()):
                        c3d = resExp.getc3d()+";\n"
                        if(len(resExp.getEV())>0):c3d+=resExp.getEV()+":"
                        if(len(resExp.getEF())>0):c3d+=resExp.getEF()+":"
                        c3d+="\n"
                    else:
                        c3d = resExp.getc3d()+";\n"
                    c3d += t1+" = p + "+str(v.getPos())+";\n"
                    c3d += "stack[int("+t1+")] = "+resExp.getValor()+";\n"                 
                    c3d += t1+" = p + "+str(v.getPos()+1)+";\n"
                    c3d += "stack[int("+t1+")] = "+str(resExp.tipo.getInt())+";\n"
                    
                    c3d += "return;\n"
                    return Primitivo("",Tipo(0),0,"","",c3d)
            TablaSimbolos.insertarError("Error sentencia fuera de llamada: "+str(resExp.getValor()),self.fila,self.columna)
            return Primitivo("",Tipo(0),0,"","","")
        
        

    def getArbol(self) -> str:
        return Nodo("return")