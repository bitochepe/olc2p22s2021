

class Funcion:

    def __init__(self,id:str,parametros,Cuerpo,entorno) -> None:
        self.cuerpo = Cuerpo
        self.parametros = parametros
        self.id = id
        self.entorno = entorno

    def getParametros(self):
        return self.parametros

    def getCuerpo(self):
        return self.cuerpo

    def getId(self):
        return self.id

    def getEntorno(self):
        return self.entorno
