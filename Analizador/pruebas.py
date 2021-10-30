
def esMultiplo(numero):
    if numero % 5==0:
        return "es multiplo de 5"
    else:
        return "no es multiplo de 5"

num=int(input("Ingrese un numero entero:"))
print(esMultiplo(num))
