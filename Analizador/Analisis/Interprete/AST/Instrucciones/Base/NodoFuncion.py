from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos

class NodoFuncion(NodoAST):

    def __init__(self,id,params,cuerpo:Cuerpo,tipo:Tipo) -> None:
        self.id = id
        self.params = params
        self.cuerpo = cuerpo
        self.tipo = tipo
        pass

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        c3d = "func "+self.id+"(){\n"
        entorno.insertarEntorno("Funcion"+self.id,self.tipo.getNombre())
        entorno.insertarVariable("$retorno$",Primitivo("",self.tipo,0,"","",""),0)
        entorno.insertarFuncion(self.id,self.params,self.cuerpo,entorno.getEtornoActual(),self.tipo)
        TablaSimbolos.insertarLlamada(self.id)
        for x in self.params:
            entorno.insertarVariable(x.getId(),Primitivo("",x.getTipo(),0,"","",""),0)
        c3d += self.cuerpo.ejecutar(entorno).getc3d()
        entorno.insertarFuncion(self.id,self.params,self.cuerpo,entorno.getEtornoActual(),self.tipo)
        entorno.eliminarEntorno()
        c3d += "return;\n}\n"
        TablaSimbolos.insertarCodigoFuncion(c3d)
        return Primitivo("",Tipo(0),0,"","","")

    def getArbol(self) -> str:
        nodo = Nodo("DECFUNC")
        nodo.addHoja(Nodo(self.id))
        nodo.addHoja(Nodo(str(self.params)))
        nodo.addHoja(self.cuerpo.getArbol())
        return nodo