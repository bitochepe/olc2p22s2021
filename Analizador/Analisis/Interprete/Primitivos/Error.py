
import datetime
class Error:

    def __init__(self,tipo,descripcion,fila,columna) -> None:
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        pass

    def getFilaReporte(self)->str:
        x = datetime.datetime.now()
        return "<tr><td>"+self.tipo+"</td>"+"<td>"+self.descripcion+"</td>"+"<td>"+str(self.fila)+"</td>"+"<td>"+str(self.columna)+"</td><td>"+x.strftime("%c")+"</td></tr>"