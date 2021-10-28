class Var:

    def __init__(self,nombre,ambito,fila,columna) -> None:
        self.nombre = nombre
        self.ambito = ambito
        self.fila = fila
        self.columna = columna
        pass

    def getFilaReporte(self)->str:
        return "<tr><td>"+self.nombre+"</td>"+"<td>"+self.ambito+"</td>"+"<td>"+str(self.fila)+"</td>"+"<td>"+str(self.columna)+"</td></tr>"