from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Entorno.Entorno import Entorno

class For(NodoAST):

    def __init__(self, id:str,exp:NodoAST, cuerpo:Cuerpo, fila, column) -> None:
        self.id  =id
        self.exp = exp
        self.cuerpo = cuerpo
        self.fila = fila
        self.columna = column

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        
        exp = self.exp.ejecutar(entorno)
        if(exp.tipo.esError()):
            TablaSimbolos.insertarError("Error en la expresion For: "+str(exp.getValor()),self.fila,self.columna)

        elif(exp.tipo.getInt()== -2):#se itera un rango e in e
            limI:Primitivo = exp.getValor()[0]
            limS:Primitivo = exp.getValor()[1]
       
            Linicio = TablaSimbolos.getNewEtiq()
            Lsalida = TablaSimbolos.getNewEtiq()
            TablaSimbolos.insertarCiclo(Linicio,Lsalida)

            t = TablaSimbolos.getNewTemp()
            TablaSimbolos.temporalUsado(t)
            c3d = limI.getc3d()+"\n"
            c3d += limS.getc3d()+"\n"
            #cambio simulado
            actual:Entorno = entorno.getEtornoActual()
            entorno.insertarEntorno("iteradorFor","-")
            entorno.insertarVariable(self.id,Primitivo(limI.getValor(),Tipo(1),0,"","",limI.getc3d()),1) #iterador

            c3d += "p = p + "+str(actual.getTam())+";\n"
            c3d += "stack[int(p)] = "+limI.getValor()+";\n"
            c3d += t+" = stack[int(p)];\n"         
            c3d += Linicio+":\n"
            c3d += "if "+t+" >= "+limS.getValor()+"{goto "+Lsalida+";}\n"

            #cambio simulado
            c3d += "p = p + 1;\n"
            entorno.insertarEntorno("cuerpoFor","-")
            resCuerpo = self.cuerpo.ejecutar(entorno)
            c3d += resCuerpo.getc3d()
            entorno.eliminarEntorno()
            #regreso a entorno anterior
            c3d += "p = p - 1;\n"
            c3d += t +" = "+t+" + 1;\n"
            c3d += "stack[int(p)] = "+t+";\n"
            c3d += "goto "+Linicio+";\n"
            c3d += Lsalida+":\n"
            entorno.eliminarEntorno()
            #regreso a entorno anterior
            c3d += "p = p - "+str(actual.getTam())+";\n"
            TablaSimbolos.sacarCiclo()

            TablaSimbolos.temporalUsado(limI.getValor())
            TablaSimbolos.temporalUsado(limS.getValor())
            TablaSimbolos.temporalUsado(t)

        # elif(exp.tipo.esString()): #Se itera un string
        #     entorno.insertarEntorno("iteradorFor","-")
        #     entorno.insertarVariable(self.id,Primitivo(0,Tipo(4),0),1)
        #     for x in exp.getValor():
        #         entorno.setValor(self.id,Primitivo(x,Tipo(4),0),Tipo(4))
        #         entorno.insertarEntorno("cuerpoFor","-")
        #         resCuerpo = self.cuerpo.ejecutar(entorno)
        #         entorno.eliminarEntorno()
        #         if(resCuerpo is not None):
        #             if(resCuerpo.tipo.esBreak()):
        #                 if(TablaSimbolos.huboCiclo()):
        #                     entorno.eliminarEntorno()
        #                     TablaSimbolos.sacarCiclo()
        #                     return None
        #                 else:
        #                     TablaSimbolos.insertarError("Llamada break fuera de un ciclo",self.fila,self.columna)
        #                     return None
        #             elif(resCuerpo.tipo.esContinue()):
        #                 pass
        #             elif(resCuerpo.tipo.esReturn()):
        #                 if(TablaSimbolos.huboLlamada()):
        #                     return resCuerpo
        #                 else:
        #                     TablaSimbolos.insertarError("Llamada return fuera de una funcion",self.fila,self.columna)
        #                     return None
        #     entorno.eliminarEntorno()
        #     return None

        else:
            TablaSimbolos.insertarError("Error en el tipo de la expresion For: "+str(exp.tipo.getNombre()),self.fila,self.columna)

        return Primitivo("",Tipo(0),0,"","",c3d)

    def getArbol(self) -> str:
        nodo = Nodo("For")
        nodo.addHoja(self.exp.getArbol())
        nodo.addHoja(self.cuerpo.getArbol())
        return nodo