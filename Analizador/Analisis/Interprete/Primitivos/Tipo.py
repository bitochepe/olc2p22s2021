
from enum import Enum, unique

class Tipo:
    #MatricesOperadores: 
    # MA = + - * / ^ %   
    # MM = *
    # MP = ^
    # MR = < > <= >= == !=
    # ML = OR AND NOT
    
    tipos={0:'NULL', 1:'INT64', 2:'FLOAT64', 3:'BOOL', 4:'CHAR', 5:'STRING', 6:'RETURN', 7:'CONTINUE', 8:'BREAK', -1:'Error'}
    matrizMA = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,1,2,-1,-1,-1,-1,-1,-1],[-1,2,2,-1,-1,-1,-1,-1,-1],
                 [-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],
                 [-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1]]

    matrizMM = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,1,2,-1,-1,-1,-1,-1,-1],[-1,2,2,-1,-1,-1,-1,-1,-1],
                 [-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,5,-1,-1,-1],
                 [-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1]]

    matrizMP = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,1,2,-1,-1,-1,-1,-1,-1],[-1,2,2,-1,-1,-1,-1,-1,-1],
                 [-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,5,-1,-1,-1,-1,-1,-1,-1],
                 [-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1]]

    matrizMR = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,3,3,-1,-1,-1,-1,-1,-1],[-1,3,3,-1,-1,-1,-1,-1,-1],
                 [-1,-1,-1,3,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,3,-1,-1,-1],
                 [-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1]]

    matrizML = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,1,2,-1,-1,-1,-1,-1,-1],[-1,2,2,-1,-1,-1,-1,-1,-1],
                 [-1,-1,-1,3,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],
                 [-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1]]


    def __init__(self,tipo):
        self.tipo = tipo
    
    @staticmethod
    def getTipo(t):
        return Tipo.tipos.get(t)

    @staticmethod
    def getTipoResultado(val1:int,val2:int,op:int)->int:
        if (op == 0):
            return Tipo.matrizMA[val1][val2]
        elif (op == 1):
            return Tipo.matrizMM[val1][val2]
        elif (op == 2):
            return Tipo.matrizMP[val1][val2]
        elif (op == 3):
            return Tipo.matrizMR[val1][val2]
        elif (op == 4):
            return Tipo.matrizML[val1][val2]
        else:
            return -1
    
    def getInt(self):
        return self.tipo

    def getNombre(self):
        return Tipo.getTipo(self.tipo)

    def esNull(self)->bool:
        return self.tipo == 0
    def esInt(self)->bool:
        return self.tipo == 1
    def esFloat(self)->bool:
        return self.tipo == 2
    def esBool(self)->bool:
        return self.tipo == 3
    def esChar(self)->bool:
        return self.tipo == 4
    def esString(self)->bool:
        return self.tipo == 5
    def esReturn(self)->bool:
        return self.tipo == 6
    def esContinue(self)->bool:
        return self.tipo == 7
    def esBreak(self)->bool:
        return self.tipo == 8
    def esError(self)->bool:
        return self.tipo == -1
    
    
@unique
class enumTipo(Enum):
    NULL : 0
    INT64 : 1
    FLOAT64 : 2
    BOOL : 3
    CHAR : 4
    STRING : 5
    RETURN : 6
    CONTINUE : 7
    BREAK : 8