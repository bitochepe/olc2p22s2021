
class Reporte:

    def __init__(self,fila,tipo,antes,despues,regla) -> None:
        self.fila = fila
        self.tipo = tipo
        self.antes = antes
        self.despues = despues
        self.regla = regla

    def getReporte(self):
        rep = "<tr>"
        rep += "<td>"+str(self.fila)+"</td>"
        rep += "<td>"+str(self.tipo)+"</td>"
        rep += "<td>"+str(self.antes)+"</td>"
        rep += "<td>"+str(self.despues)+"</td>"
        rep += "<td>"+str(self.regla)+"</td>"
        rep += "</tr>"
        return rep