from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Nodo import Nodo

class Asignacion(NodoAST):

    def __init__(self,id:str,valor:NodoAST,tipo:Tipo,ambito:int,fila:int,columna:int,palabra:bool) -> None:
        self.id = id
        self.valor = valor
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.ambito = ambito
        self.palabra = palabra

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        c3d = ""
        if(self.valor is None): #si el valor de la expresion no fue especificado, ocurre cuando se usa local o global
            if(self.ambito): #se declaro para el ambito global con la palabra reservada "global"
                aux = entorno.getValorGlobal(self.id)
                if(aux is None):#La variable no existe
                    entorno.insertarVariableGlobal(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                    entorno.insertarVariable(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                    c3d += "stack[int("+str(entorno.getEtornoGlobal().getTam()-1)+")] = 0;\n"
                    c3d += "stack[int("+str(entorno.getEtornoActual().getTam()-1)+")] = 0;\n"
                else: #la variable ya existia
                    aux2 = entorno.getValor(self.id)
                    entorno.setValorGlobal(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                    entorno.setValor(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                    c3d += "stack[int("+str(aux.getPos())+")] = 0;\n"
                    if(aux2 is not None):
                        t = TablaSimbolos.getNewTemp()
                        c3d += t+" = p + "+str(aux2.getPos())
                        c3d += ";\nstack[int("+t+")] = 0;\n"

            else: #Se declaro la variable en ambito local 
                if(self.palabra):
                    aux = entorno.getValorLocal(self.id)
                    if(aux is None): #No existe la variable
                        entorno.insertarVariable(self.id,Primitivo("",Tipo(0),0,"","",""),0)
                        t = TablaSimbolos.getNewTemp()
                        c3d += t+" = p + "+str(entorno.getEtornoActual().getTam()-1)
                        c3d += ";\nstack[int("+t+")] = 0;\n"
                
                    else: #La variable ya existia
                        TablaSimbolos.insertarError("No es declarar dos veces la misma variable: \""+str(self.id)+"\"")
                        return Primitivo("",Tipo(0),0,"","",c3d)
                else:
                    aux = entorno.getValor(self.id)
                    if(aux is None): #No existe la variable
                        entorno.insertarVariable(self.id,Primitivo("",Tipo(0),0,"","",""),0)
                        t = TablaSimbolos.getNewTemp()
                        c3d += t+" = p + "+str(entorno.getEtornoActual().getTam()-1)
                        c3d += ";\nstack[int("+t+")] = 0;\n"
                
                    else: #La variable ya existia
                        if(aux.tipo == 1): #se declaro la varible en un entorno global pero hace referencia a una global
                            entorno.setValorGlobal(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                            entorno.setValor(self.id,Primitivo("",Tipo(0),0,"","",""),1)
                            c3d += "stack[int("+str(aux.getPos())+")] = 0;\n"
                            aux2 = entorno.getValorGlobal(self.id)
                            if(aux2 is not None):
                                t = TablaSimbolos.getNewTemp()
                                c3d += t+" = p + "+str(aux2.getPos())+";\n"
                                c3d += ";\nstack[int("+t+")] = 0;\n" 

                        else:   #en ambito local
                            entorno.setValor(self.id,Primitivo("",Tipo(0),0,"","",""),0)
                            t = TablaSimbolos.getNewTemp()
                            c3d += t+" = p + "+str(aux.getPos())
                            c3d += ";\nstack[int("+t+")] = 0;\n"
                 
        
        #el valor de la expresion fue especificado
        else:        
            exp = self.valor.ejecutar(entorno)
            if(exp.tipo.esError()):
                TablaSimbolos.insertarError(exp.getValor(),self.fila,self.columna)
                return Primitivo("",Tipo(0),0,"","",c3d)

            if(self.ambito): #Se declaro en el entorno global
                aux = entorno.getValorGlobal(self.id)
                if(aux is None): #La variable no existe
                    if(self.tipo is None): #el tipo no fue especificado
                        entorno.insertarVariableGlobal(self.id,exp,1)
                        entorno.insertarVariable(self.id,exp,1)
                        c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                        c3d += "stack[int("+str(entorno.getEtornoGlobal().getTam()-1)+")] = "+exp.getValor()+";\n"
                        t = TablaSimbolos.getNewTemp()
                        c3d += t+" = p + "+str(entorno.getEtornoActual().getTam()-1)
                        c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"

                    else: #el tipo fue declarado
                        if(self.tipo.getInt() == exp.tipo.getInt()):
                            entorno.insertarVariableGlobal(self.id,exp,1)
                            entorno.insertarVariable(self.id,exp,1)
                            c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                            c3d += "stack[int("+str(entorno.getEtornoGlobal().getTam()-1)+")] = "+exp.getValor()+";\n"
                            t = TablaSimbolos.getNewTemp()
                            c3d += t+" = p + "+str(entorno.getEtornoActual().getTam()-1)
                            c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"

                        else: #El tipo de la expresion no coincide con el especificado
                            TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"")
                            return Primitivo("",Tipo(0),0,"","",c3d)

                else: #La variable existe 
                    if(self.tipo is None):   #tipo no especificado                   
                        entorno.setValorGlobal(self.id,exp,0)
                        c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                        c3d += "stack[int("+str(aux.getPos())+")] = "+exp.getValor()+";\n"

                    else: #tipo especificado
                        if(self.tipo.getTipo() == exp.tipo.getInt()): #Los tipos coinciden
                            entorno.setValorGlobal(self.id,exp,0)
                            c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                            c3d += "stack[int("+str(aux.getPos())+")] = "+exp.getValor()+";\n"

                        else: #los tipos no coinciden
                            TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"")
                            return Primitivo("",Tipo(0),0,"","",c3d)
            else: #El ambito es local
                if(self.palabra):
                    aux = entorno.getValorLocal(self.id)
                    if(aux is None): #la variable no existe
                        if(self.tipo is None): #no se especifico tipo
                            entorno.insertarVariable(self.id,exp,0)
                            c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                            t = TablaSimbolos.getNewTemp()
                            c3d += t+" = p + "+str(entorno.getEtornoActual().getTam()-1)
                            c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"
                    
                        else: #se especifico tipo
                            if(self.tipo.getInt() == exp.tipo.getInt()):
                                entorno.insertarVariable(self.id,exp,0)
                                c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                                t = TablaSimbolos.getNewTemp()
                                c3d += t+" = p + "+str(entorno.getEtornoActual().getTam()-1)
                                c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"
                        
                            else: #los tipos no coinciden
                                TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"",self.fila,self.columna)
                                return Primitivo("",Tipo(0),0,"","",c3d)

                    else: #La variable existe
                        TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"",self.fila,self.columna)          
                        return Primitivo("",Tipo(0),0,"","",c3d)
                else:
                    aux = entorno.getValor(self.id)
                    if(aux is None): #la variable no existe
                        if(self.tipo is None): #no se especifico tipo
                            entorno.insertarVariable(self.id,exp,0)
                            c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                            t = TablaSimbolos.getNewTemp()
                            c3d += t+" = p + "+str(entorno.getEtornoActual().getTam()-1)
                            c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"
                    
                        else: #se especifico tipo
                            if(self.tipo.getInt() == exp.tipo.getInt()):
                                entorno.insertarVariable(self.id,exp,0)
                                c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                                t = TablaSimbolos.getNewTemp()
                                c3d += t+" = p + "+str(entorno.getEtornoActual().getTam()-1)
                                c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"
                        
                            else: #los tipos no coinciden
                                TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"",self.fila,self.columna)
                                return Primitivo("",Tipo(0),0,"","",c3d)
                    else: #La variable existe
                        if(aux.tipo == 1): #es referencia a global
                            if(self.tipo is None): #no se especifica tipo
                                entorno.setValorGlobal(self.id,exp,1)
                                entorno.setValor(self.id,exp,1)
                                c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                                c3d += "stack[int("+str(aux.getPos())+")] = "+exp.getValor()+";\n"
                                aux2 = entorno.getValorGlobal(self.id)
                                if(aux2 is not None):
                                    t = TablaSimbolos.getNewTemp()
                                    c3d += t+" = p + "+str(aux2.getPos())
                                    c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"
                    
                            else: #se especifica tipo
                                if(aux.getTipo() == exp.tipo.getInt()):
                                    entorno.setValorGlobal(self.id,exp,1)
                                    entorno.setValor(self.id,exp,1)
                                    c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                                    c3d += "stack[int("+str(aux.getPos())+")] = "+exp.getValor()+";\n"
                                    aux2 = entorno.getValorGlobal(self.id)
                                    if(aux2 is not None):
                                        t = TablaSimbolos.getNewTemp()
                                        c3d += t+" = p + "+str(aux2.getPos())
                                        c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"
                                
                                else: #No coiciden los itpos
                                    TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"",self.fila,self.columna)          
                                    return Primitivo("",Tipo(0),0,"","",c3d)
                        
                        else: #entorno local
                            if(self.tipo is None): #no se especifica tipo
                                entorno.setValor(self.id,exp,0)
                                c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                                t = TablaSimbolos.getNewTemp()
                                c3d += t+" = p + "+str(aux.getPos())
                                c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"
                            
                            else: #Se especifica tipo
                                if(aux.getTipo() == exp.tipo.getInt()):
                                    entorno.setValor(self.id,exp,0)
                                    c3d += exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
                                    t = TablaSimbolos.getNewTemp()
                                    c3d += t+" = p + "+str(aux.getPos())
                                    c3d += ";\nstack[int("+t+")] = "+exp.getValor()+";\n"

                                else:
                                    TablaSimbolos.insertarError("No es posible asignar valor, se asigno: \""+str(exp.tipo.getNombre())+"\" y se esperaba: \""+str(self.tipo.getNombre())+"\"",self.fila,self.columna)          
                                    return Primitivo("",Tipo(0),0,"","",c3d)

        for x in TablaSimbolos.listavars:
            if(x == self.id):
                return Primitivo("",Tipo(0),0,"","",c3d)
        TablaSimbolos.addVar(self.id)
        return Primitivo("",Tipo(0),0,"","",c3d)
                  
    def getArbol(self) -> str:
        nodo = Nodo('Asignacion')
        nodo.addHoja(Nodo(self.id))
        nodo.addHoja(self.valor.getArbol())
        return nodo

    def setValor(self,exp,hayExp):

        if(hayExp >0):
            c3d = exp.getc3d()+"\n"+self.id+" = "+exp.getValor()+";\n"
            c3d += "stack[int(p)] = "+exp.getValor()+";\n"
        return c3d
