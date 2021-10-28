
import re
from Analisis.Interprete.AST.Nodo import Nodo

class Raiz:

    def __init__(self,lerrores,ltokens,insts) -> None:
        self.dot = ""
        self.lerrores = lerrores
        self.ltokens = ltokens
        self.insts = insts
        self.contador = 0

    def getArbol(self):
        self.contador = 0
        try:
            nodo = Nodo("S")
            for x in self.insts:
                nodo.addHoja(x.getArbol())
            self.getDot(nodo)
            return self.dot
        except:
            return "digraph ast{ Error \n}"

    def getDot(self,raiz:Nodo):
        try:
            self.dot = ""
            self.dot += "digraph ast{\n"
            self.dot += 'n0[label="' + raiz.getDato() + '"];\n'
            self.contador = 1
            self.getNodos("n0",raiz)
            self.dot += "}"
        except:
            self.dot = "Error en intentar traer:"+str(raiz.getDato())

    def getNodos(self,number:str,nodo:Nodo):
        try:
            for x in nodo.getHojas():
                hijo = "n"+str(self.contador)
                self.contador += 1
                self.dot += hijo + '[label="' + str(x.getDato()) + '"];\n'
                self.dot += number + "->" + hijo + ";\n"
                self.getNodos(hijo,x)
        except Exception as e:
            print("Error except: "+str(e))
            pass