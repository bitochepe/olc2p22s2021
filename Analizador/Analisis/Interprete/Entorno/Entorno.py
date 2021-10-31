
from Analisis.Interprete.Entorno.Simbolo import Simbolo
class Entorno:

    def __init__(self,nombre,tipo) -> None:
        self.nombre = nombre
        self.tabla = {}
        self.tipo = tipo

    def insertarVariable(self,nombre:str,variable:Simbolo):
        if(self.tabla.get(nombre) is not None):
            variable.ambito = self.nombre
            self.tabla[nombre] = variable
        else:
            variable.ambito = self.nombre
            variable.pos = len(self.tabla)
            self.tabla[nombre] = variable

    def getVariable(self,nombre:str) -> Simbolo:
        return self.tabla.get(nombre,None)

    def getNombre(self):
        return self.nombre
    
    def getTS(self):
        vars = [*self.tabla]
        rep = "<tr><td>"+str(self.nombre)+"</td>"+"<td>"+str(self.tipo)+"</td><td>-</td><td>Metodo</td><td>-</td><td>"+str(len(self.tabla))+"</td></tr>"
        for i in vars:
            aux:Simbolo = self.tabla.get(i)
            rep += "<tr>"
            rep += "<td>"+str(i)+"</td>"
            rep += "<td>"+str(aux.valor.tipo.getNombre())+"</td>"
            rep += "<td>"+str(self.nombre)+"</td>"
            rep += "<td>"+str(aux.rol)+"</td>"
            rep += "<td>"+str(aux.pos)+"</td>"
            rep += "<td>"+str(aux.tam)+"</td>"
            rep += "</tr>"
        return rep

    def getTam(self):
        return len(self.tabla)