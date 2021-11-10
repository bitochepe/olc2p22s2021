
from Analisis.Interprete.AST.Instrucciones.Base.Funcion import Funcion
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.Primitivos.Error import Error
from Analisis.Interprete.Entorno.Entorno import Entorno
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.Entorno.Simbolo import Simbolo
from Analisis.Interprete.Primitivos.Var import Var


class TablaSimbolos:

    salidaConsola = ""
    decvariables = "var t0"
    repTS = []
    listaErrores = []
    display = []
    llamadas = []
    etiqActual = 0
    tempActual = 0
    listavars = []
    codigoFunciones = ""
    listaTemporales = []

    def __init__(self) -> None:
        self.listaEntornos = [Entorno]
        self.listaMetodos = {}

    def insertarEntorno(self,nombre:str,tipo):
        nuevo = Entorno(nombre,tipo)
        self.listaEntornos.insert(0,nuevo)

    def insertarEntornoE(self,entorno):
        self.listaEntornos.insert(0,entorno)

    def eliminarEntorno(self):
        return self.listaEntornos.pop(0)
    
    def getEtornoActual(self)->Entorno:
        return self.listaEntornos[0]

    def getEtornoGlobal(self)->Entorno:
        return self.listaEntornos[len(self.listaEntornos-2)]

    def insertarVariable(self,nombre:str, valor:Primitivo,tipo:int):
        if(self.listaEntornos[0].getVariable(nombre) is not None):
            return False
        else:
            nueva = Simbolo(tipo,valor,"",0,"Variable local",1)
            self.listaEntornos[0].insertarVariable(nombre,nueva)
            TablaSimbolos.repTS.append(Var(nombre,self.listaEntornos[0].getNombre(),0,0))
            return True

    def getValor(self,nombre:str) -> Simbolo:
        n = len(self.listaEntornos)-1
        i = 0
        while(i<n):
            if(self.listaEntornos[i].getVariable(nombre) is not None):
                return self.listaEntornos[i].getVariable(nombre)
            else:
                i = i+1
        return None

    def getPtrLess(self,nombre:str) -> int:
        n = len(self.listaEntornos)-1
        i = 0
        s = 0

        if(self.listaEntornos[i].getVariable(nombre) is not None):
            return s
        i = i + 1

        while(i<n):
            if(self.listaEntornos[i].getVariable(nombre) is not None):
                s = s + self.listaEntornos[i].getTam()
                return s
            else:
                s = s + self.listaEntornos[i].getTam()
                i = i+1
        return s

    def getValorLocal(self,nombre:str) -> Simbolo:     
        if(self.listaEntornos[0].getVariable(nombre) is not None):
            return self.listaEntornos[0].getVariable(nombre)
        return None

    def setValor(self,nombre:str,valor:Primitivo,tipo:int):
        n = len(self.listaEntornos)-1
        i = 0
        while(i<n):
            if(self.listaEntornos[i].getVariable(nombre) is not None):               
                nuevo = Simbolo(tipo,valor,"",0,"Variable local",1)
                self.listaEntornos[i].insertarVariable(nombre,nuevo)
                break
            else:
                i = i+1
    
    def getValorGlobal(self,nombre:str) -> Simbolo:
            if(self.listaEntornos[(len(self.listaEntornos)-2)].getVariable(nombre) is not None):
                return self.listaEntornos[(len(self.listaEntornos)-2)].getVariable(nombre)
            else:
                return None

    def setValorGlobal(self,nombre:str,valor:Primitivo,tipo:int):
        nuevo = Simbolo(tipo,valor,"",0,"Variable local",1)
        self.listaEntornos[(len(self.listaEntornos)-2)].insertarVariable(nombre,nuevo)
        return True

    def insertarVariableGlobal(self,nombre:str, valor:Primitivo,tipo:int):
        if(self.listaEntornos[(len(self.listaEntornos)-2)].getVariable(nombre) is not None):
            return False
        else:
            nueva = Simbolo(tipo,valor,"",0,"Variable local",1)
            self.listaEntornos[-1].insertarVariable(nombre,nueva)
            TablaSimbolos.repTS.append(Var(nombre,self.listaEntornos[0].getNombre(),0,0))
            return True

    def insertarFuncion(self,id:str,parametros,cuerpo:Cuerpo,entorno:Entorno):
        self.listaMetodos[id] = Funcion(id,parametros,cuerpo,entorno)

    def existeFuncion(self,id:str) -> Funcion:
        if(self.listaMetodos.get(id,None) is not None):
            return self.listaMetodos.get(id)
        return None

    def getTablaSimbolos(self):
        rep = '<table class="table table-hover" style="cellpadding="0" cellspacing="0" width="80%""><tr style="font-weight: bold; background: lightblue;"><td>Nombre</td><td>Tipo</td><td>Ambito</td><td>Rol</td><td>Posicion</td><td>Tamaño</td></tr>'  
        i = 0
        n = len(self.listaEntornos)-2
        while(n>=i):
            rep += self.listaEntornos[n].getTS()
            n -= 1
        rep += "</table>"
        return rep

    @staticmethod
    def insertarTemporales(tg,tt):
        TablaSimbolos.listaTemporales.append([tg,tt])
    
    @staticmethod
    def sacarTemporales():
        return TablaSimbolos.listaTemporales.pop()

    @staticmethod  
    def insertarLlamada(id:str):
        TablaSimbolos.llamadas.append(id)

    @staticmethod
    def sacarLlamada():
        if(len(TablaSimbolos.llamadas)>0):
            return TablaSimbolos.llamadas.pop()

    @staticmethod
    def huboLlamada():
        return len(TablaSimbolos.llamadas) > 0

    @staticmethod
    def insertarCiclo(Linicio:str,Lsalida):
        TablaSimbolos.display.append([Linicio,Lsalida])

    @staticmethod
    def sacarCiclo():
        return TablaSimbolos.display.pop()

    @staticmethod
    def huboCiclo():
        return len(TablaSimbolos.display) > 0

    @staticmethod
    def insertarError(valor:str,fila:int,columna:int):
        TablaSimbolos.listaErrores.append(Error('Semantico',valor,fila,columna))

    @staticmethod
    def insertarSalida(valor:str):
        TablaSimbolos.salidaConsola += valor+"\n"

    @staticmethod
    def insertarCodigoFuncion(valor:str):
        TablaSimbolos.codigoFunciones += valor+"\n"

    @staticmethod
    def getErrores():
        res = ""
        for x in TablaSimbolos.listaErrores:
            res += x.getFilaReporte()
        return res
    
    @staticmethod
    def getTS():
        res = ""
        for x in TablaSimbolos.repTS:
            res += x.getFilaReporte()
        res = '<table class="table table-hover" style="cellpadding="0" cellspacing="0" width="80%""><tr style="font-weight: bold; background: lightblue;"><td>Nombre</td><td>Ambito</td><td>Fila</td><td>Columna</td></tr>"+res+"</table>'
        return res 
    
    @staticmethod
    def getNewTemp():
        TablaSimbolos.tempActual += 1
        TablaSimbolos.decvariables += ", t"+str(TablaSimbolos.tempActual)
        return "t"+str(TablaSimbolos.tempActual)
    
    @staticmethod
    def getNewEtiq():
        TablaSimbolos.etiqActual += 1
        return "L"+str(TablaSimbolos.etiqActual)

    @staticmethod
    def reinicio():
        TablaSimbolos.salidaConsola = ""
        TablaSimbolos.decvariables = "var t0"
        TablaSimbolos.repTS = []
        TablaSimbolos.listaErrores = []
        TablaSimbolos.display = []
        TablaSimbolos.llamadas = []
        TablaSimbolos.etiqActual = 0
        TablaSimbolos.tempActual = 0
        TablaSimbolos.listavars = []
        TablaSimbolos.codigoFunciones = ""
        TablaSimbolos.listaTemporales = []
    
    @staticmethod
    def addVar(var):
        TablaSimbolos.listavars.append(var)

    @staticmethod
    def printBoolean(valor):
        if(valor==0):
            return "fmt.Printf(\"%c\", int(70));\nfmt.Printf(\"%c\", int(65));\nfmt.Printf(\"%c\", int(76));\nfmt.Printf(\"%c\", int(83));\nfmt.Printf(\"%c\", int(69));\n"
        else:
            return "fmt.Printf(\"%c\", int(84));\nfmt.Printf(\"%c\", int(82));\nfmt.Printf(\"%c\", int(85));\nfmt.Printf(\"%c\", int(69));\n"