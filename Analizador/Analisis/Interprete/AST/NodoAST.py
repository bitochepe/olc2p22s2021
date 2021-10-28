

from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from abc import ABC, abstractmethod

class NodoAST(ABC):

    @abstractmethod
    def ejecutar(self,entorno)->Primitivo:
        pass

    @abstractmethod
    def getArbol(self)->str:
        pass