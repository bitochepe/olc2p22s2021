
llamada = []

llamada.append("funcionA")

if(len(llamada)>0):
    aux = llamada.pop()
else:
    aux = None

if(len(llamada)>0):
    aux2 = llamada.pop()
else:
    aux2 = None
if(aux is not None):
    print(aux)
else:
    print("aux es Nada")
if(aux2 is not None):
    print(aux2)
else:
    print("aux2 es Nada")
