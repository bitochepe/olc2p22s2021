

class Funcion:

    def __init__(self,id:str,parametros,Cuerpo) -> None:
        self.cuerpo = Cuerpo
        self.parametros = parametros
        self.id = id

    def getParametros(self):
        return self.parametros

    def getCuerpo(self):
        return self.cuerpo

    def getId(self):
        return self.id
