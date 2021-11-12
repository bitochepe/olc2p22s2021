
class NodoOPT():

    def __init__(self,id,opi,opd,op,tipo) -> None:
        self.id = id
        self.opi = opi
        self.opd = opd
        self.op = op
        self.tipo = tipo

    def getCodigo(self):
        if(self.tipo == 1):
            return str(self.id)+" = "+str(self.opi)+str(self.op)+str(self.opd)+";"
        if(self.tipo == 1.3):
            return str(self.id)+"[int("+str(self.opi)+")] = "+str(self.opd)+";"
        if(self.tipo == 1.6):
            return str(self.id) + " = "+str(self.opi)+"[int("+str(self.opd)+")];"
        if(self.tipo == 1.9):
            return str(self.id)+" = "+str(self.opi)+";"
        if(self.tipo == 2):
            return str(self.id)+":"
        if(self.tipo == 3):
            return "goto "+str(self.id)+";"
        if(self.tipo == 4):
            return "fmt.Printf(\""+str(self.id)+"\","+str(self.op)+");"
        if(self.tipo == 4.5):
            return "fmt.Printf(\""+str(self.id)+"\",int("+str(self.op)+"));"
        if(self.tipo == 5):
            return "if "+str(self.opi)+str(self.op)+str(self.opd)+" {goto "+str(self.id)+";}"
        if(self.tipo == 6):
            return str(self.id)+"();"
        if(self.tipo == 7):
            return "return;"
        
        