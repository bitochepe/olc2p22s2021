from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Raiz import Raiz
from Analisis.Interprete.AST.Instrucciones.Base.Inicial import Inicial
import Analisis.gramatica as gramatica

#imports temporales de prueba:


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
    ts.insertarEntorno("global",0,"void")
    i = Inicial()
    cf = i.ejecutar(ts)
    for x in ltokens:
        x.ejecutar(ts)
        
    raiz = Raiz(lerrores,None,ltokens)
    dot = raiz.getArbol()
    rts = TablaSimbolos.getTS()
    res = "package main;\nimport(\"fmt\");\nvar p, h float64;\nvar stack[100000]float64;\nvar heap[100000]float64;\n"+TablaSimbolos.decvariables + " float64;\n"
    res += cf + "func main(){\n"+TablaSimbolos.salidaConsola+"}"
    errS = TablaSimbolos.getErrores()
    
    for x in lerrores:
        errS += x.getFilaReporte()
    errS = "<table class=\"table table-hover\"><tr><td>Tipo</td><td>Descripcion</td><td>Fila</td><td>Columna</td></tr>"+errS+"</table>"

    TablaSimbolos.reinicio()
    #borrando saltos de linea de mas
    res = res.replace("\n\n","\n") 
    res = res.replace("\n\n","\n")
    res = res.replace("\n\n","\n")
    res = res.replace("\n\n","\n")
    print(res) #linea temporal
    print(errS) #linea temporal
    print(ts.getTablaSimbolos()) #linea temporal
    return {'dot' : dot, 'rts' : rts, 'res' : res, 'estado':'true', 'errS':errS}

f = open("./entrada.txt", "r")
input = f.read()
Analizar2(input)