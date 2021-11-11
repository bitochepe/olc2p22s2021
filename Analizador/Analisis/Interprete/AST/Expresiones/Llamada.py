
from math import tau
from typing import List
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.Nodo import Nodo

class Llamada(NodoAST):

    def __init__(self,id,parametros:List[NodoAST],fila,columna) -> None:
        self.id = id
        self.parametros = parametros
        self.fila = fila
        self.columna = columna

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        
        funcion = entorno.existeFuncion(self.id)
        if(funcion is not None):
            if(len(self.parametros) == len(funcion.parametros)):
                actual = entorno.getEtornoActual()
                entorno.insertarEntornoE(funcion.getEntorno())
                c3d = ""
                try:
                    #guardar temporales no usados
                    auxtemps = []
                    for x in TablaSimbolos.tempNoUsados:
                        if(x=="$"):break
                        auxtemps.append(x)
                    
                    for y in auxtemps:
                        taux = TablaSimbolos.getNewTemp()
                        TablaSimbolos.temporalUsado(taux)
                        c3d += taux+" = p + "+str(actual.getTam())+";\n"
                        c3d += "stack[int("+taux+")] = "+y+";\n"
                        entorno.insertarVariable(y,Primitivo("",Tipo(0),0,"","",""),0)
                    TablaSimbolos.tempNoUsados.insert(0,"$")

                    it = 0
                    for x in self.parametros:
                        auxE = entorno.eliminarEntorno()
                        aux = x.ejecutar(entorno)
                        if(aux.tipo.esError()):
                            return Primitivo("Error en parametros en la llamada a la funcion "+str(self.id),Tipo(-1),0,"","","")
                        elif(aux.tipo.getInt() != funcion.parametros[it].getTipo().getInt()):
                            return Primitivo("Error en el tipo de un parametro en la llamada a la funcion "+str(self.id),Tipo(-1),0,"","","")
                        else:
                            #insertar valor en el nuevo entrono a ejecutar (cambio simulado)
                            t = TablaSimbolos.getNewTemp()
                            t2 = TablaSimbolos.getNewTemp()
                            c3d += aux.getc3d()+"\n"
                            c3d += t +" = p + "+str(actual.getTam())+";\n"
                            c3d += t2 + " = "+t+" + "+str(it+1)+";\n"
                            c3d += "stack[int("+t2+")] = "+aux.getValor()+";\n"
                            TablaSimbolos.temporalUsado(t2)
                            TablaSimbolos.temporalUsado(t)
                            TablaSimbolos.temporalUsado(aux.getValor())
                            #insertar variable en el entorno
                            entorno.insertarEntornoE(auxE)
                            entorno.insertarVariable(funcion.parametros[it].getId(),aux,0)
                            it = it + 1
        
                    c3d += "p = p + "+str(actual.getTam())+";\n"
                    c3d += funcion.id+"();\n"
                    
                    #capturar el valor de retorno   
                    tr = TablaSimbolos.getNewTemp() #temporal para la posicion del retorno
                    tg = TablaSimbolos.getNewTemp() #temporal para el valor de retrono

                    #Se guarda el valor del retorno 
                    c3d += tr+" = p + 0;\n"
                    c3d += tg+ " = stack[int("+tr+")];\n"
                    c3d += "p = p - "+str(actual.getTam())+";\n" #retorno al ambito anterior
                    TablaSimbolos.temporalUsado(tr)

                    #regresar valores guardados antes de la llamda
                    for z in auxtemps:
                        tmp = entorno.getValor(z)
                        taux = TablaSimbolos.getNewTemp()
                        TablaSimbolos.temporalUsado(taux)
                        c3d += taux+" = p + "+str(tmp.getPos())+";\n"
                        c3d += z +" = stack[int("+taux+")];\n"

                    v = entorno.getValor("$retorno$")
                    
                    entorno.eliminarEntorno()
                    return Primitivo(tg,v.getValor().tipo,0,v.getValor().getEV(),v.getValor().getEF(),c3d)

                except:
                    return Primitivo('Error en servidor al correr funcion',Tipo(-1),0,"","","")
            else:
                return Primitivo("Parametros mal definido para la funcion \""+str(self.id)+"\"",Tipo(-1),0,"","","")
        else:
            return Primitivo("Funcion \""+str(self.id)+"\" no definida",Tipo(-1),0,"","","")

    def getArbol(self) -> str:
        nodo = Nodo("Llamada")
        nodo.addHoja(Nodo(self.id))
        return nodo


