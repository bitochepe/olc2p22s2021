#imports de todos los archivos para el analisis

from Analisis.Optimizacion.NodoOPT import NodoOPT

#variables globales de utilidad
lerrores = []
entrada = ""
reservadas = {
    'func' : 'Rfunc',
    'fmt' : 'Rfmt',
    'Printf' : 'Rprint',
    'int' : 'Rint',
    'float64' : 'Rfloat64',
    'goto' : 'Rgoto',
    'if' : 'Rif',
    'var' : 'Rvar',
    'return' : "Rreturn"
}

tokens  = [
    'pyc',
	'dospuntos',
    'coma',
    'parA',
    'parC',
	'corA',
    'corC',
    'llaveA',
    'llaveC',
    'igual',
    'mas',
    'menos',
    'por',
    'div',
    'mayq',
    'meq',
    'mayiq',
    'meiq',
    'iqiq',
	'noiq',
    'entero',
    'decimal',
    'identificador',
    'cadena',
    'encabezado',
    'punto'
] + list(reservadas.values())

# Tokens
t_pyc = r';'
t_dospuntos = r':'
t_punto = r'\.'
t_coma = r','
t_parA = r'\('
t_parC = r'\)'
t_corA = r'\['
t_corC = r'\]'
t_llaveA = r'\{'
t_llaveC = r'\}'
t_igual = r'='
t_mas = r'\+'
t_menos = r'-'
t_por = r'\*'
t_div = r'/'
t_mayiq = r'>='
t_meiq = r'<='
t_mayq = r'>'
t_meq = r'<'
t_iqiq = r'=='
t_noiq = r'!='
t_encabezado = r'package main;\nimport("fmt");\nvar p, h float64;\nvar stack[100000]float64;\nvar heap[100000]float64;'

def t_decimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_identificador(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'identificador')
     return t

def t_entero(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_cadena(t):
    r'\".*?\"'
    t.value = t.value[1:-1] #se toma el texto sin comillas
    return t 

t_ignore = " \t\r"

def t_newline(t):
     r'\n+'
     t.lexer.lineno += t.value.count("\n")

def t_error(t):
    
    lerrores.append("Error en linea")
    t.lexer.skip(1)

def find_column(token,pos):
    line_start = entrada.rfind('\n', token) + 1
    return (pos - line_start) + 1

# Construyendo el analizador sintactico
from ply import lex as lex
lexer = lex.lex()


# Definición de la gramática
def p_S(t):
    '''S : LFUNC'''
    t[0] = {'tokens':t[1], 'errores': lerrores}

def p_LFUNC(t):
    '''LFUNC : LFUNC FUNCION
            | FUNCION'''
    if(t.slice[1].type == 'LFUNC'):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_FUNCION(t):
    '''FUNCION : Rfunc identificador parA parC llaveA CUERPO llaveC'''
    t[0] = NodoOPT(t[6],"","",t[2],"")

def p_CUERPO(t):
    'CUERPO : LINS'
    t[0] = t[1]

def p_LINS(t):
    '''LINS : LINS INS
            | INS'''
    if(t.slice[1].type == 'LINS'):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]
    
    #tipo: ASIGNA : 1, ASIGNARSTACKHEAP TMP : 1.3, ASIGNAR A TMP STACKHEAP :1.6 TMP = TMP : 1.9, 
    #ETIQUETA: 2, SALTO: 3, PRINT: 4, IF: 5, LLAMADA: 6
def p_INS(t):
    '''INS : ASIGNA
            | ETIQUETA
            | SALTO
            | PRINT
            | IF
            | LLAMADA
            | RETORNO'''
    t[0] = t[1]

def p_ASIGNA(t):
    '''ASIGNA : identificador igual E pyc
            | identificador igual PRIMITIVO pyc
            | identificador corA Rint parA PRIMITIVO parC corC igual PRIMITIVO pyc
            | identificador igual identificador corA Rint parA PRIMITIVO parC corC pyc'''
    if(t.slice[3].type == 'E'):
        t[3].id = t[1]
        t[3].tipo = 1
        t[0] = t[3]
    elif(t.slice[3].type == 'PRIMITIVO'):
        t[0] = NodoOPT(t[1],t[3],"","",1.9)     
    elif(t.slice[3].type == 'Rint'):
        t[0] = NodoOPT(t[1],t[5],t[9],"",1.3)
    elif(t.slice[3].type == 'identificador'):
        t[0] = NodoOPT(t[1],t[3],t[7],"",1.6)

def p_ETIQUETA(t):
    '''ETIQUETA : identificador dospuntos'''
    t[0] = NodoOPT(t[1],"","","",2)

def p_SALTO(t):
    '''SALTO : Rgoto identificador pyc'''
    t[0] = NodoOPT(t[2],"","","",3)

def p_PRINT(t):
    '''PRINT : Rfmt punto Rprint parA cadena coma PRIMITIVO parC pyc
             | Rfmt punto Rprint parA cadena coma Rint parA PRIMITIVO parC parC pyc'''
    if(t.slice[7].type == 'PRIMITIVO'):
        t[0] = NodoOPT(t[5],"","",t[7],4)
    elif(t.slice[7].type == 'Rint'):
        t[0] = NodoOPT(t[5],"","",t[9],4.5)

def p_IF(t):
    '''IF : Rif E llaveA SALTO llaveC
            | Rif parA E parC llaveA SALTO llaveC'''
    if(t.slice[2].type == 'E'):
        t[2].tipo = 5
        t[2].id = t[4].id
        t[0] = t[2]
    elif(t.slice[2].type == 'parA'):
        t[3].tipo = 5
        t[3].id = t[6].id
        t[0] = t[3]

def p_LLAMADA(t):           
    '''LLAMADA : identificador parA parC pyc'''
    t[0] = NodoOPT(t[1],"","","",6)

def p_RETORNO(t):           
    '''RETORNO : Rreturn pyc'''
    t[0] = NodoOPT(t[1],"","","",7)
                 
def p_E(t):
    '''E :  PRIMITIVO mas PRIMITIVO
          | PRIMITIVO menos PRIMITIVO
          | PRIMITIVO por PRIMITIVO
          | PRIMITIVO div PRIMITIVO
          | PRIMITIVO meq PRIMITIVO
          | PRIMITIVO mayq PRIMITIVO
          | PRIMITIVO meiq PRIMITIVO
          | PRIMITIVO mayiq PRIMITIVO
          | PRIMITIVO iqiq PRIMITIVO
          | PRIMITIVO noiq PRIMITIVO'''

    if(t.slice[1].type == 'menos'):
        t[0] = NodoOPT("","",t[2],t[1],1)
    elif(t.slice[1].type == 'mas'):
        t[0] = NodoOPT("","",t[2],t[1],1)
    elif(t.slice[2].type == 'mas'):
        t[0] = NodoOPT("",t[1],t[3],t[2],1)
    elif(t.slice[2].type == 'menos'):
        t[0] = NodoOPT("",t[1],t[3],t[2],1)
    elif(t.slice[2].type == 'por'):
        t[0] = NodoOPT("",t[1],t[3],t[2],1)
    elif(t.slice[2].type == 'div'):
        t[0] = NodoOPT("",t[1],t[3],t[2],1)
    
    
    # 0:> 1:< 2:>= 3:<= 4:== 5:!=
    elif(t.slice[2].type == 'mayq'):
        t[0] = NodoOPT("",t[1],t[3],">",1)
    elif(t.slice[2].type == 'meq'):
        t[0] = NodoOPT("",t[1],t[3],str(t[2]),1)
    elif(t.slice[2].type == 'mayiq'):
        t[0] = NodoOPT("",t[1],t[3],t[2],1)
    elif(t.slice[2].type == 'meiq'):
        t[0] = NodoOPT("",t[1],t[3],t[2],1)
    elif(t.slice[2].type == 'iqiq'):
        t[0] = NodoOPT("",t[1],t[3],t[2],1)
    elif(t.slice[2].type == 'noiq'):
        t[0] = NodoOPT("",t[1],t[3],t[2],1)


def p_Primitivo(t):
    '''PRIMITIVO : entero
                    | decimal
                    | identificador
                    | menos entero
                    | menos decimal'''
    if(t.slice[1].type == 'entero'):
        t[0] = t[1]
    elif(t.slice[1].type == 'decimal'):
        t[0] = t[1]
    elif(t.slice[1].type == 'identificador'):
        t[0] = t[1]
    elif(t.slice[1].type == 'menos'):
        t[0] = "-"+str(t[2])
def p_error(t):
    print(t)
    lerrores.append("Sintactico, No se esperaba el token: "+str(t.value))

from ply import yacc as yacc
parser = yacc.yacc()


def parse(input) :
    global lexer
    global entrada
    entrada = input
    input = input.replace("\r","")
    lexer = lex.lex()
    return parser.parse(input)