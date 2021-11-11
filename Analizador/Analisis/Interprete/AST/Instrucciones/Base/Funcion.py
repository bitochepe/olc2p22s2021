

from Analisis.Interprete.Entorno.Simbolo import Simbolo


class Funcion:

    def __init__(self,id:str,parametros,Cuerpo,entorno,tipo) -> None:
        self.cuerpo = Cuerpo
        self.parametros = parametros
        self.id = id
        self.entorno = entorno
        self.tipo = tipo

    def getParametros(self):
        return self.parametros

    def getCuerpo(self):
        return self.cuerpo

    def getId(self):
        return self.id

    def getEntorno(self):
        return self.entorno

    def getTipo(self)->Simbolo:
        return self.tipo