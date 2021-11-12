from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Optimizacion.Reporte import Reporte

class Mirilla():

    def __init__(self,funciones) -> None:
        self.funciones = funciones
    
    def generarCodigo(self):
        salida = ""
        for x in self.funciones:
            z = x.id
            salida +="func "+str(x.op)+"(){\n"
            for y in z:
                salida += y.getCodigo()+"\n"
            salida += "}\n"
        return salida

    def optimizar(self):
        self.Regla1()
        self.Regla2()
        self.Regla3()
        self.Regla4()
        self.Regla5()
        self.Regla6()
        self.Regla7()
        self.Regla8()
        return self.generarCodigo()

    def Regla1(self):
        it = 8
        pos = 0
        for x in self.funciones:
            fin = len(x.id)
            it += 1
            for y in x.id:
                if(y.tipo == 1.9):
                    pos += 1
                    aux = pos
                    while(aux < fin):
                        if(x.id[aux].id == y.opi and y.id == x.id[aux].opi and x.id[aux].opd == "" and y.opd == "" ):
                            TablaSimbolos.listaMirilla.append(Reporte(it,"Mirilla",y.getCodigo()+"\n"+x.id[aux].getCodigo(),y.getCodigo(),"1"))
                            x.id.remove(x.id[aux])
                            fin -= 1
                            aux += 1
                            break
                        elif(x.id[pos].tipo == 2):
                            break
                        aux += 1
            it += 1
        pass

    def Regla2(self):
        it = 8
        auxit = 0
        aux = None
        lista = []
        for x in self.funciones:
            it += 1
            for y in x.id:
                if(aux is not None and y.tipo != 2):
                    lista.append(y)
                if(y.tipo == 3):
                    aux = y
                    lista = []
                    auxit = it

                if(y.tipo == 2 and aux is not None):
                    if(aux.id == y.id):
                        cantes = ""
                        for a in lista:
                            cantes += a.getCodigo()+"\n"
                            if(a.tipo == 3):
                                for r in x.id:
                                    if(r.id == a.id):
                                        x.id.remove(r)
                                        break
                            x.id.remove(a)
                        x.id.remove(aux)
                        x.id.remove(y)

                        TablaSimbolos.listaMirilla.append(Reporte(auxit,"Mirilla",aux.getCodigo()+cantes,y.getCodigo(),"2"))
                        aux = None
                        lista = []
                    else:
                        aux = None
                        lista = []
                        aux = None    
                it += 1
            it += 1
        pass
    
    def Regla3(self):
        pass
    
    def Regla4(self):
        pass
    
    def Regla5(self):
        pass
    
    def Regla6(self):
        it = 8
        for x in self.funciones:
            it += 1
            for y in x.id:
                if(y.id == y.opi and (y.op == "+" or y.op == "-") and y.opd == 0):
                    cantes = y.getCodigo()
                    y.opd = ""
                    y.op = ""
                    TablaSimbolos.listaMirilla.append(Reporte(it,"Mirilla",cantes,y.getCodigo(),"6"))
                if(y.id == y.opi and (y.op == "*" or y.op == "/") and y.opd == 1):
                    cantes = y.getCodigo()
                    y.opd = ""
                    y.op = ""
                    TablaSimbolos.listaMirilla.append(Reporte(it,"Mirilla",cantes,y.getCodigo(),"6"))
                it += 1
            it += 1
        pass
    
    def Regla7(self):
        it = 8
        for x in self.funciones:
            it += 1
            for y in x.id:
                if((y.op == "+" or y.op == "-") and y.opd == 0):
                    cantes = y.getCodigo()
                    y.opd = ""
                    y.op = ""
                    TablaSimbolos.listaMirilla.append(Reporte(it,"Mirilla",cantes,y.getCodigo(),"7"))
                if((y.op == "*" or y.op == "/") and y.opd == 1):
                    cantes = y.getCodigo()
                    y.opd = ""
                    y.op = ""
                    TablaSimbolos.listaMirilla.append(Reporte(it,"Mirilla",cantes,y.getCodigo(),"7"))
                it += 1
            it += 1
        pass
    
    def Regla8(self):
        it = 8
        for x in self.funciones:
            it += 1
            for y in x.id:
                if((y.op == "*") and y.opd == 2):
                    cantes = y.getCodigo()
                    y.opd = y.opi
                    y.op = "+"
                    TablaSimbolos.listaMirilla.append(Reporte(it,"Mirilla",cantes,y.getCodigo(),"8"))
                elif((y.op == "*") and y.opd == 0):
                    cantes = y.getCodigo()
                    y.opd = ""
                    y.op = ""
                    TablaSimbolos.listaMirilla.append(Reporte(it,"Mirilla",cantes,y.getCodigo(),"8"))
                elif((y.op == "/") and y.opi == 0):
                    cantes = y.getCodigo()
                    y.opd = ""
                    y.op = ""
                    y.opi = 0
                    TablaSimbolos.listaMirilla.append(Reporte(it,"Mirilla",cantes,y.getCodigo(),"8"))
                it += 1
            it += 1
        pass