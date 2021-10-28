from types import resolve_bases
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.Primitivos.Primitivo import Primitivo


class Simbolo:

    def __init__(self,tipo:int,valor:Primitivo,ambito:str,pos:int,rol:str,tam:int) -> None:
        self.valor = valor
        self.tipo =  tipo #si es variable global o local
        self.ambito = ambito
        self.rol = rol
        self.pos = pos
        self.tam = tam

    def getValor(self)-> Primitivo:
        return self.valor

    def setValor(self,valor:Primitivo)->Primitivo:
        self.valor = valor

    def getTipo(self)-> int:
        return self.tipo
    
    def setTipo(self,tipo:int)->None:
        self.tipo = tipo

    def getAmbito(self)-> str:
        return self.ambito
    
    def getPos(self)->int:
        return self.pos

    def getTam(self)->int:
        return self.tam
