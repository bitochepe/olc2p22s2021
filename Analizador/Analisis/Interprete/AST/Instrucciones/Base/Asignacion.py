import re
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Asignacion(NodoAST):

    def __init__(self,id:str,valor:NodoAST,tipo:Tipo,ambito:int,fila:int,columna:int) -> None:
        self.id = id
        self.valor = valor
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.ambito = ambito

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        
        if(self.valor is None): #si el valor de la expresion no fue especificado, ocurre cuando se usa local o global
            if(self.ambito):
                aux = entorno.getValorGlobal(self.id)
                if(aux is None):
                    entorno.insertarVariableGlobal(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                    entorno.insertarVariable(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                else:
                    entorno.setValorGlobal(self.id,aux.getValor(),1)
                    entorno.setValor(self.id,aux.getValor(),1)
            else:
                aux = entorno.getValor(self.id)
                if(aux is None):
                    entorno.insertarVariable(self.id,Primitivo("",Tipo(0),0,"","",""),0)                
                else:
                    if(aux.tipo == 1):
                        entorno.setValorGlobal(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                        entorno.setValor(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                    else:    
                        entorno.setValor(self.id,Primitivo("",Tipo(0),0,"","",""),0)
        
        #el valor de la expresion fue especificado
        else:        
            exp = self.valor.ejecutar(entorno)
            if(exp.tipo.esError()):
                TablaSimbolos.insertarError(exp.getValor(),self.fila,self.columna)
                return None

            if(self.ambito):
                aux = entorno.getValorGlobal(self.id)
                if(aux is None):
                    if(self.tipo is None):
                        entorno.insertarVariableGlobal(self.id,exp,1)
                        entorno.insertarVariable(self.id,exp,1)
                    else:
                        if(self.tipo.getInt() == exp.tipo.getInt()):
                            entorno.insertarVariableGlobal(self.id,exp,1)
                            entorno.insertarVariable(self.id,exp,1)
                        else:
                            TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"")
                            return None
                else:
                    if(self.tipo is None):                      
                        entorno.setValorGlobal(self.id,exp,0)
                    else:
                        if(self.tipo.getTipo() == exp.tipo.getInt()):
                            entorno.setValorGlobal(self.id,exp,0)
                        else:
                            TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"")
                            return None
            else:
                aux = entorno.getValor(self.id)
                if(aux is None):
                    if(self.tipo is None):
                        entorno.insertarVariable(self.id,exp,0)
                    else:
                        if(self.tipo.getInt() == exp.tipo.getInt()):
                            entorno.insertarVariable(self.id,exp,0)
                        else:
                            TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"",self.fila,self.columna)
                            return None
                else:
                    if(aux.tipo == 1):
                        if(self.tipo is None):
                            entorno.setValorGlobal(self.id,exp,1)
                            entorno.setValor(self.id,exp,1)
                        else:
                            if(aux.getTipo() == exp.tipo.getInt()):
                                entorno.setValorGlobal(self.id,exp,1)
                                entorno.setValor(self.id,exp,1)
                            else:
                                TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"",self.fila,self.columna)          
                                return None
                    else:
                        if(self.tipo is None):
                            entorno.setValor(self.id,exp,0)
                        else:
                            if(aux.getTipo() == exp.tipo.getInt()):
                                entorno.setValor(self.id,exp,0)
                            else:
                                TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"",self.fila,self.columna)          
                                return None
        TablaSimbolos.insertarSalida(exp.getc3d())
        return None           

    def getArbol(self) -> str:
        nodo = Nodo('Asignacion')
        nodo.addHoja(Nodo(self.id))
        nodo.addHoja(self.valor.getArbol())
        return nodo