
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Raiz import Raiz
from Analisis.Interprete.AST.Instrucciones.Base.Inicial import Inicial
import Analisis.gramatica as gramatica

def Analizar(entrada:str):
    rs = gramatica.parse(entrada+' ')
    ltokens = rs.get('tokens')
    lerrores = rs.get('errores')

    ts = TablaSimbolos()
    ts.insertarEntorno("global")
    i = Inicial()
    i.ejecutar(ts)

    for x in ltokens:
        x.ejecutar(ts)
        
    raiz = Raiz(lerrores,None,ltokens)
    dot = raiz.getArbol()
    rts = TablaSimbolos.getTS()
    res = TablaSimbolos.salidaConsola
    errS = TablaSimbolos.getErrores()
    
    for x in lerrores:
        errS += x.getFilaReporte()
    errS = "<table class=\"table table-hover\"><tr><td>Tipo</td><td>Descripcion</td><td>Fila</td><td>Columna</td></tr>"+errS+"</table>"


    TablaSimbolos.salidaConsola = ""
    TablaSimbolos.listaErrores = []
    TablaSimbolos.display = []
    TablaSimbolos.llamadas = []
    TablaSimbolos.repTS = []
    return {'dot' : dot, 'rts' : rts, 'res' : res, 'estado':'true', 'errS':errS}
    
def Analizar2(entrada:str):
    rs = gramatica.parse(entrada+' ')
    ltokens = rs.get('tokens')
    lerrores = rs.get('errores')

    ts = TablaSimbolos()
    ts.insertarEntorno("global","void")
    i = Inicial()
    cf = i.ejecutar(ts)
    for x in ltokens:
        TablaSimbolos.insertarSalida(x.ejecutar(ts).getc3d())

    cf += TablaSimbolos.codigoFunciones 
    raiz = Raiz(lerrores,None,ltokens)
    dot = raiz.getArbol()
    rts = TablaSimbolos.getTS()
    for y in TablaSimbolos.listavars:
        TablaSimbolos.decvariables += ", "+str(y)
    res = "package main;\nimport(\"fmt\");\nvar p, h float64;\nvar stack[100000]float64;\nvar heap[100000]float64;\n"+TablaSimbolos.decvariables + " float64;\n"
    res += cf + "func main(){\n"+TablaSimbolos.salidaConsola+"}"
    errS = TablaSimbolos.getErrores()
    
    for x in lerrores:
        errS += x.getFilaReporte()
    errS = '<table class="table table-hover" style="cellpadding="0" cellspacing="0" width="80%""><tr style="font-weight: bold; background: red;"><td>Tipo</td><td>Descripcion</td><td>Fila</td><td>Columna</td></tr>'+errS+'</table>'

    TablaSimbolos.reinicio()
    #borrando saltos de linea de mas
    res = res.replace("\n\n","\n") 
    res = res.replace("\n\n","\n")
    res = res.replace("\n\n","\n")
    res = res.replace("\n\n","\n")
    print("===================ERROREs==========================")
    print(errS) #linea temporal
    print("===================TABLA SIMBOLOS==========================")
    print(ts.getTablaSimbolos()) #linea temporal

    #linea teporales
    f = open("C:\\Users\\bitochepe\\Desktop\\olc2p2\\olc2p22s2021\\Analizador\\salida.txt", "w")
    f.write(res)
    f.close()

    return {'dot' : dot, 'rts' : rts, 'res' : res, 'estado':'true', 'errS':errS}

f = open("C:\\Users\\bitochepe\\Desktop\\olc2p2\\olc2p22s2021\\Analizador\\entrada.txt", "r")
input = f.read()
Analizar2(input)