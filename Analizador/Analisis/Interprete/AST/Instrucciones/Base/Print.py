from typing import List
from Analisis.Interprete.Entorno.TablaSimbolos import TablaSimbolos
from Analisis.Interprete.AST.NodoAST import NodoAST
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Nodo import Nodo
from Analisis.Interprete.Primitivos.Tipo import Tipo

class Print(NodoAST):

    def __init__(self,fila:int,columna:int,exp:List[NodoAST],salto) -> None:
        self.fila = fila
        self.columna = columna
        self.exp = exp
        self.salto = salto

    def ejecutar(self, entorno:TablaSimbolos) -> Primitivo:
        c3d = ""
        for x in self.exp:
            expRes = x.ejecutar(entorno)
            if(expRes.tipo.esBool()):
                etiqSalida = TablaSimbolos.getNewEtiq()
                c3d += expRes.getc3d()+";\n"
                if(len(expRes.getEV())>0): c3d += expRes.getEV()+":"
                c3d += TablaSimbolos.printBoolean(1)
                c3d += "goto "+etiqSalida+";\n"
                if(len(expRes.getEF())>0): c3d += expRes.getEF()+":"
                c3d += TablaSimbolos.printBoolean(0)
                c3d += etiqSalida+":\n"

            elif(expRes.tipo.esFloat()):
                c3d += expRes.getc3d()
                c3d += "fmt.Printf(\"%f\", "+expRes.getValor()+");\n"

            elif(expRes.tipo.esChar()):
                c3d += expRes.getc3d()
                c3d += "fmt.Printf(\"%c\", int("+expRes.getValor()+"));\n"

            elif(expRes.tipo.esInt()):
                c3d += expRes.getc3d()
                c3d += "fmt.Printf(\"%d\", int("+expRes.getValor()+"));\n"

            elif(expRes.tipo.esString()):
                c3d += expRes.getc3d()
                t = TablaSimbolos.getNewTemp()
                t2 = TablaSimbolos.getNewTemp()
                codigo = t+" = p + 1;\n"+t2+" = stack[int("+t+")];\n"+"stack[int("+t+")] = "+expRes.getValor()+";\nprintString();\n"+"stack[int("+t+")] = "+t2+";\n"
                c3d += codigo

            elif(expRes.tipo.esBreak() or expRes.tipo.esContinue() or expRes.tipo.esNull()):
                #nuevo error semantico
                TablaSimbolos.insertarError("Sentencia break o continue dentro de print no admitida",self.fila,self.columna)

            elif(expRes.tipo.esReturn()):
                c3d += expRes.getc3d()

                etqs = TablaSimbolos.getNewEtiq()
                etqi = TablaSimbolos.getNewEtiq()
                etqf = TablaSimbolos.getNewEtiq()
                etqc = TablaSimbolos.getNewEtiq()
                etqstr = TablaSimbolos.getNewEtiq()
                etqb = TablaSimbolos.getNewEtiq()

                c3d += "if("+expRes.getValor()[1]+"== 0){goto "+etqs+";}\n"
                c3d += "if("+expRes.getValor()[1]+"== 1){goto "+etqi+";}\n"
                c3d += "if("+expRes.getValor()[1]+"== 2){goto "+etqf+";}\n"
                c3d += "if("+expRes.getValor()[1]+"== 3){goto "+etqb+";}\n"
                c3d += "if("+expRes.getValor()[1]+"== 4){goto "+etqc+";}\n"
                c3d += "if("+expRes.getValor()[1]+"== 5){goto "+etqstr+";}\n"
                c3d += "goto "+etqs+";\n"

                #bool
                c3d += etqb+":\n"
                c3d += expRes.getValor()[2].getc3d()+"\n"
                etiqSalida = TablaSimbolos.getNewEtiq()
                if(len(expRes.getValor()[2].getEV())>0): c3d += expRes.getEV()+":"
                c3d += TablaSimbolos.printBoolean(1)
                c3d += "goto "+etiqSalida+";\n"
                if(len(expRes.getValor()[2].getEF())>0): c3d += expRes.getEF()+":"
                c3d += TablaSimbolos.printBoolean(0)
                c3d += etiqSalida+":\n"
                c3d += "goto "+etqs+";\n"

                #float
                c3d += etqf+":\n"
                #c3d += expRes.getValor()[2].getc3d()
                c3d += "fmt.Printf(\"%f\", "+expRes.getValor()[0]+");\n"
                c3d += "goto "+etqs+";\n"

                #char
                c3d += etqc+":\n"
                #c3d += expRes.getValor()[2].getc3d()
                c3d += "fmt.Printf(\"%c\", int("+expRes.getValor()[0]+"));\n"
                c3d += "goto "+etqs+";\n"

                #int
                c3d += etqi+":\n"
                #c3d += expRes.getValor()[2].getc3d()
                c3d += "fmt.Printf(\"%d\", int("+expRes.getValor()[0]+"));\n"
                c3d += "goto "+etqs+";\n"

                #string
                c3d += etqstr+":\n"
                t = TablaSimbolos.getNewTemp()
                t2 = TablaSimbolos.getNewTemp()
                codigo = t+" = p + 1;\n"+t2+" = stack[int("+t+")];\n"+"stack[int("+t+")] = "+expRes.getValor()[0]+";\nprintString();\n"+"stack[int("+t+")] = "+t2+";\n"
                c3d += codigo
                c3d += "goto "+etqs+";\n"

                #fin
                c3d += etqs+":\n"

            elif(expRes.tipo.esNull()):
                TablaSimbolos.insertarError("El valor de la variable es NUll",self.fila,self.columna)
            else:
                #error semantico
                TablaSimbolos.insertarError(expRes.getValor(),self.fila,self.columna)
                
        if(self.salto): c3d += "fmt.Printf(\"%c\", 10);\n"      
        return Primitivo("",Tipo(0),0,"","",c3d)

    def getArbol(self):
        nodo = Nodo("Print")
        for x in self.exp:
            nodo.addHoja(x.getArbol())
        return nodo