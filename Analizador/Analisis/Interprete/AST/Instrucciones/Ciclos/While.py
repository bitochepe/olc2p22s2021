
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.Entorno.Entorno import Entorno
from Analisis.Interprete.Primitivos.Tipo import Tipo

class While(NodoAST):

    def __init__(self, exp:NodoAST, cuerpo:Cuerpo, fila, column) -> None:
        self.exp = exp
        self.cuerpo = cuerpo
        self.fila = fila
        self.columna = column

    def ejecutar(self, entorno: TablaSimbolos) -> Primitivo:
        
        c3d = ""
        exp = self.exp.ejecutar(entorno)
        if(exp.tipo.esError()):
            TablaSimbolos.insertarError("Error en la expresion while: "+str(exp.getValor()),self.fila,self.columna)

        elif(exp.tipo.esBool()):
            Linicio = TablaSimbolos.getNewEtiq()
            Lsalida = TablaSimbolos.getNewEtiq()
            TablaSimbolos.insertarCiclo(Linicio,Lsalida)

            #Cambio simulado
            actual:Entorno = entorno.getEtornoActual()
            c3d += "p = p + "+str(actual.getTam())+";\n"

            #nuevo entorno y traduccion de while
            entorno.insertarEntorno('while',"-")
            resCuerpo = self.cuerpo.ejecutar(entorno)
            c3d += Linicio+":\n"
            exp = self.exp.ejecutar(entorno)
            c3d += exp.getc3d()+"\n"+exp.getEV()+":\n"
            c3d += resCuerpo.getc3d()
            c3d += "goto "+Linicio+";\n"
            c3d += exp.getEF()+":\ngoto "+Lsalida+";\n"
            c3d += Lsalida+":\n"
            entorno.eliminarEntorno()
            #regreso a entorno anterior
            c3d += "p = p - "+str(actual.getTam())+";\n"
            TablaSimbolos.temporalUsado(exp.getValor())
            TablaSimbolos.sacarCiclo()
        else:
            TablaSimbolos.insertarError("Error en el tipo de la expresion while: "+str(exp.tipo.getNombre()),self.fila,self.columna)

        return Primitivo("",Tipo(0),0,"","",c3d)

    def getArbol(self) -> str:
        nodo = Nodo("WHILE")
        nodo.addHoja(self.exp.getArbol())
        nodo.addHoja(self.cuerpo.getArbol())
        return nodo