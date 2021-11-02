#imports de todos los archivos para el analisis

from Analisis.Interprete.AST.Instrucciones.Base.NodoFuncion import NodoFuncion
from Analisis.Interprete.AST.Expresiones.Llamada import Llamada
from Analisis.Interprete.AST.Instrucciones.Ciclos.For import For
from Analisis.Interprete.Primitivos.Primitivo import Primitivo
from Analisis.Interprete.AST.Instrucciones.Base.Print import Print
from Analisis.Interprete.AST.Expresiones.Eprimitivo import Eprimitivo
from Analisis.Interprete.Primitivos.Error import Error
from Analisis.Interprete.Primitivos.Tipo import Tipo
from Analisis.Interprete.AST.Expresiones.Aritmeticas.Suma import Suma
from Analisis.Interprete.AST.Expresiones.Aritmeticas.Division import Division
from Analisis.Interprete.AST.Expresiones.Aritmeticas.Resta import Resta
from Analisis.Interprete.AST.Expresiones.Aritmeticas.Multiplicacion import Multiplicacion
from Analisis.Interprete.AST.Expresiones.Aritmeticas.Modular import Modular
from Analisis.Interprete.AST.Expresiones.Aritmeticas.Potencia import Potencia
from Analisis.Interprete.AST.Expresiones.Aritmeticas.Unario import Unario
from Analisis.Interprete.AST.Expresiones.Relacionales.Relacional import Relacional
from Analisis.Interprete.AST.Expresiones.Logicas.Logica import Logica  
from Analisis.Interprete.AST.Expresiones.Eid import Eid
from Analisis.Interprete.AST.Instrucciones.Sentencias.If import If
from Analisis.Interprete.AST.Instrucciones.Cuerpo import Cuerpo
from Analisis.Interprete.AST.Instrucciones.Base.Asignacion import Asignacion
from Analisis.Interprete.AST.Instrucciones.Ciclos.While import While
from Analisis.Interprete.AST.Expresiones.inF import inF
from Analisis.Interprete.AST.Instrucciones.Sentencias.Break import Break
from Analisis.Interprete.AST.Instrucciones.Sentencias.Continue import Continue
from Analisis.Interprete.AST.Instrucciones.Sentencias.Return import Return


#variables globales de utilidad
lerrores = []
entrada = ""
reservadas = {
    'Int64'	: 'Rint',
    'Float64' : 'Rfloat',
    'Bool' : 'Rbool',
    'Char'	: 'Rchar',
    'String' : 'Rstring',
    'nothing' : 'Rnothing',
    'print' : 'Rprint',
    'println' : 'Rprintln',
    'true' : 'Rtrue',
    'false' : 'Rfalse',
    'if' : 'Rif',
    'else' : 'Relse',
    'end' : 'Rend',
    'elseif':'Relseif',
    'local' : 'Rlocal',
    'global' : 'Rglobal',
    'while' : 'Rwhile',
    'for' : 'Rfor',
    'in' : 'Rin',
    'break' : 'Rbreak',
    'continue' : 'Rcontinue',
    'return' : 'Rreturn',
    'function' : 'Rfunction'
}

tokens  = [
    'pyc',
	'dospuntos',
    'coma',
    'parA',
    'parC',
	'corA',
    'corC',
    'igual',
    'mas',
    'menos',
    'por',
    'div',
    'modular',
    'potencia',
    'mayq',
    'meq',
    'mayiq',
    'meiq',
    'iqiq',
	'noiq',
    'and',
	'or',
    'not',
    'entero',
    'decimal',
    'cadenaS',
    'cadenaC',
    'identificador'
] + list(reservadas.values())


# Tokens
t_pyc = r';'
t_dospuntos = r':'
t_coma = r','
t_parA = r'\('
t_parC = r'\)'
t_corA = r'\['
t_corC = r'\]'
t_igual = r'='
t_mas = r'\+'
t_menos = r'-'
t_por = r'\*'
t_div = r'/'
t_modular = r'%'
t_potencia = r'\^'
t_mayiq = r'>='
t_meiq = r'<='
t_mayq = r'>'
t_meq = r'<'
t_iqiq = r'=='
t_noiq = r'!='
t_and = r'&&'
t_or = r'\|\|'
t_not = r'!'

t_ignore_comentarioM =  r'\#\=[^\=]\#'
t_ignore_comentarioS = r'\#.*'

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

def t_cadenaC(t):
    r'\'[a-zA-ZñÑ]\''
    t.value = t.value[1:-1] #se toma el texto sin comillas
    return t 

def t_cadenaS(t):
    r'\".*?\"'
    t.value = t.value[1:-1] #se toma el texto sin comillas
    return t 

t_ignore = " \t\r"

def t_newline(t):
     r'\n+'
     t.lexer.lineno += t.value.count('\n')

def t_error(t):
    lerrores.append(Error('Lexico','Caracter no valido: '+t.value[0],t.lexer.lineno,find_column(t.lexer.lineno,t.lexer.lexpos)))
    t.lexer.skip(1)

def find_column(token,pos):
    line_start = entrada.rfind('\n', token) + 1
    return (pos - line_start) + 1

# Construyendo el analizador sintactico
from ply import lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','or'),
    ('left','and'),
    ('left','mayq','meq','mayiq','meiq','iqiq','noiq'),
    ('left','mas','menos'),
    ('left','por','div','modular'),
    ('right','potencia'),
    ('right','unaria','not'),
    ('left', 'parA')
    )

# Definición de la gramática
def p_S(t):
    'S : CUERPO '
    t[0] = {'tokens':t[1], 'errores': lerrores}

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
    
def p_INS(t):
    '''INS : PRINT  
            | PIF
            | ASIGNACION
            | WHILE
            | FOR
            | TRANSFERENCIA
            | DECFUNC
            | LLAMADA pyc'''
    t[0] = t[1]

def p_DECFUNC(t):
    '''DECFUNC : Rfunction identificador parA LPARF parC LINS Rend pyc'''
    t[0] = NodoFuncion(t[2],t[4],Cuerpo(t[6]))


def p_LPARF(t):
    '''LPARF : LPARF coma identificador
              | identificador
              | empty'''

    if(t.slice[1].type == "LPARF"):
        t[1].append(t[3])
        t[0] = t[1]
    elif(t.slice[1].type == 'identificador'):
        t[0] = [t[1]]
    elif(t.slice[1].type == 'empty'):
        t[0] = []

def p_TRANSFERENCIA(t):
    '''TRANSFERENCIA : Rbreak pyc
                     | Rcontinue pyc
                     | Rreturn pyc
                     | Rreturn E pyc'''

    if(t.slice[1].type == 'Rbreak'):
        t[0] = Break(t.lineno(0),find_column(t.lineno(0),t.lexpos(0)))
    elif(t.slice[1].type == 'Rcontinue'):
        t[0] = Continue(t.lineno(0),find_column(t.lineno(0),t.lexpos(0)))
    elif(t.slice[1].type == 'Rreturn'):
        if(t.slice[2].type == 'pyc'):
            t[0] = Return(None,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)))
        elif(t.slice[2].type == 'E'):
            t[0] = Return(t[2],t.lineno(0),find_column(t.lineno(0),t.lexpos(0)))

def p_FOR(t):
    '''FOR : Rfor identificador Rin FORE LINS Rend pyc'''
    t[0] = For(t[2],t[4],Cuerpo(t[5]),t.lineno(0),find_column(t.lineno(0),t.lexpos(0)))

def p_FORE(t):
    ''' FORE : E dospuntos E
              | cadenaS
              | identificador'''
    if(t.slice[1].type == 'E'):
        t[0] = inF(t[1],t[3])
    elif(t.slice[1].type == 'cadenaS'):
        t[0] = Eprimitivo(t[1],Tipo(5),0)
    elif(t.slice[1].type == 'identificador'):
        t[0] = Eid(t[1],t.lineno(0),find_column(t.lineno(0),t.lexpos(0)))

def p_WhHILE(t):
    '''WHILE : Rwhile E LINS Rend pyc'''
    t[0] = While(t[2],Cuerpo(t[3]),t.lineno(0),find_column(t.lineno(0),t.lexpos(0)))

def p_DECLARACION(t):
    '''ASIGNACION : identificador igual E dospuntos dospuntos TIPO pyc
                   | Rlocal identificador igual E dospuntos dospuntos TIPO pyc
                   | Rglobal identificador igual E dospuntos dospuntos TIPO pyc
                   | Rlocal identificador igual E pyc 
                   | Rglobal identificador igual E pyc
                   | identificador igual E pyc
                   | Rlocal identificador pyc
                   | Rglobal identificador pyc'''
                   
    
    if(t.slice[1].type == 'identificador'):
        if(t.slice[4].type == 'pyc'):
            t[0] = Asignacion(t[1],t[3],None,False,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)),False)
        elif(t.slice[4].type == 'dospuntos'):
            t[0] = Asignacion(t[1],t[3],t[6],False,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)),False)
    elif(t.slice[1].type == 'Rlocal'):
        if(t.slice[3].type == 'pyc'):
            t[0] = Asignacion(t[2],None,None,False,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)),True)
        elif(t.slice[5].type == 'dospuntos'):
            t[0] = Asignacion(t[2],t[4],t[7],False,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)),True)
        elif(t.slice[5].type == 'pyc'):
            t[0] = Asignacion(t[2],t[4],None,False,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)),True)
        
    elif(t.slice[1].type == 'Rglobal'):
        if(t.slice[3].type == 'pyc'):
            t[0] = Asignacion(t[2],None,None,True,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)),True)
        elif(t.slice[5].type == 'dospuntos'):
            t[0] = Asignacion(t[2],t[4],t[7],True,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)),True)
        elif(t.slice[5].type == 'pyc'):
            t[0] = Asignacion(t[2],t[4],None,True,t.lineno(0),find_column(t.lineno(0),t.lexpos(0)),True)

def p_TIPO(t):
    '''
    TIPO : Rint
    | Rfloat
    | Rbool
    | Rchar
    | Rstring
    | Rnothing
    '''
    if(t.slice[1].type == 'Rint'):
        t[0] = Tipo(1)
    elif(t.slice[1].type == 'Rfloat'):
        t[0] = Tipo(2)
    elif(t.slice[1].type == 'Rbool'):
        t[0] = Tipo(3)
    elif(t.slice[1].type == 'Rchar'):
        t[0] = Tipo(4)
    elif(t.slice[1].type == 'Rstring'):
        t[0] = Tipo(5)
    elif(t.slice[1].type == 'Rnothing'):
        t[0] = Tipo(0)
    else:
        t[0] = Tipo(-1)

def p_PIF(t):
    '''PIF : Rif E LINS Rend pyc
           | Rif E LINS Relse LINS Rend pyc
           | Rif E LINS IFELSE'''
    if(t.slice[4].type == 'Rend'):
        t[0] = If(Cuerpo(t[3]),None,t[2],t.lineno(1),find_column(t.lineno(1),t.lexpos(1)))
    elif(t.slice[4].type == 'Relse'):
        t[0] = If(Cuerpo(t[3]),Cuerpo(t[5]),t[2],t.lineno(1),find_column(t.lineno(1),t.lexpos(1)))
    elif(t.slice[4].type == 'IFELSE'):
        t[0] = If(Cuerpo(t[3]),Cuerpo([t[4]]),t[2],t.lineno(1),find_column(t.lineno(1),t.lexpos(1)))
    else:
        t[0] = Eprimitivo("Error al intentar leer if",Tipo(-1),0)

def p_IFELSE(t):
    '''
    IFELSE : Relseif E LINS Rend pyc
            | Relseif E LINS Relse LINS Rend pyc
            | Relseif E LINS IFELSE
    '''
    if(t.slice[4].type == 'Rend'):
        t[0] = If(Cuerpo(t[3]),None,t[2],t.lineno(1),find_column(t.lineno(1),t.lexpos(1)))
    elif(t.slice[4].type == 'Relse'):
        t[0] = If(Cuerpo(t[3]),Cuerpo(t[5]),t[2],t.lineno(1),find_column(t.lineno(1),t.lexpos(1)))
    elif(t.slice[4].type == 'IFELSE'):
        t[0] = If(Cuerpo(t[3]),Cuerpo([t[4]]),t[2],t.lineno(1),find_column(t.lineno(1),t.lexpos(1)))
    else:
        t[0] = Eprimitivo("Error al intentar leer if",Tipo(-1),0)
def p_PRINT(t):
    '''PRINT :  PRINTTIPO parA LES parC pyc'''
    if(t[1]==1):
        t[0] = Print(t.lineno(1),find_column(t.lineno(1),t.lexpos(1)),t[3],True)
    else:
        t[0] = Print(t.lineno(1),find_column(t.lineno(1),t.lexpos(1)),t[3],False)

def p_LES(t):
    '''LES : LES coma E
            | E'''

    if(t.slice[1].type == 'LES'):
        t[1].append(t[3])
        t[0] = t[1]
    elif(t.slice[1].type == 'E'):
        t[0] = [t[1]]

def p_PRINTTIPO(t):
    '''PRINTTIPO : Rprint
                    | Rprintln'''
    if(t.slice[1].type == 'Rprint'):
        t[0] = 0
    else:
        t[0] = 1
                 
def p_E(t):
    '''E :  E mas E
          | E menos E
          | E por E
          | E div E
          | E modular E
          | E potencia E %prec potencia
          | E meq E
          | E mayq E
          | E meiq E
          | E mayiq E
          | E iqiq E
          | E noiq E
          | E and E
          | E or E
          | not E %prec not
          | menos E %prec unaria
          | PRIMITIVO'''

    if(t.slice[1].type == 'PRIMITIVO'):
        t[0] = t[1]      
    elif(t.slice[1].type == 'not'):
        t[0] = Logica(None,t[2],2)
    elif(t.slice[1].type == 'menos'):
        t[0] = Unario(t[2],False)
    elif(t.slice[1].type == 'mas'):
        t[0] = Unario(t[2],True)
    elif(t.slice[2].type == 'mas'):
        t[0] = Suma(t[3],t[1])
    elif(t.slice[2].type == 'menos'):
        t[0] = Resta(t[3],t[1])
    elif(t.slice[2].type == 'por'):
        t[0] = Multiplicacion(t[3],t[1])
    elif(t.slice[2].type == 'div'):
        t[0] = Division(t[3],t[1])
    elif(t.slice[2].type == 'modular'):
        t[0] = Modular(t[3],t[1])
    elif(t.slice[2].type == 'potencia'):
        t[0] = Potencia(t[3],t[1])
    
    # 0:> 1:< 2:>= 3:<= 4:== 5:!=
    elif(t.slice[2].type == 'mayq'):
        t[0] = Relacional(t[3],t[1],0)
    elif(t.slice[2].type == 'meq'):
        t[0] = Relacional(t[3],t[1],1)
    elif(t.slice[2].type == 'mayiq'):
        t[0] = Relacional(t[3],t[1],2)
    elif(t.slice[2].type == 'meiq'):
        t[0] = Relacional(t[3],t[1],3)
    elif(t.slice[2].type == 'iqiq'):
        t[0] = Relacional(t[3],t[1],4)
    elif(t.slice[2].type == 'noiq'):
        t[0] = Relacional(t[3],t[1],5)
    elif(t.slice[2].type == 'and'):
        t[0] = Logica(t[3],t[1],1)
    elif(t.slice[2].type == 'or'):
        t[0] = Logica(t[3],t[1],0)
    else:
        t[0] = Eprimitivo('error else produccion E',Tipo(-1),0)

def p_Primitivo(t):
    '''PRIMITIVO : parA E parC
                    | entero
                    | decimal
                    | cadenaS
                    | cadenaC
                    | Rtrue
                    | Rfalse
                    | identificador
                    | LLAMADA'''
    if(t.slice[1].type == 'entero'):
        t[0] = Eprimitivo(t[1],Tipo(1),0)
    elif(t.slice[1].type == 'decimal'):
        t[0] = Eprimitivo(t[1],Tipo(2),0)
    elif(t.slice[1].type == 'cadenaC'):
        t[0] = Eprimitivo(t[1],Tipo(4),0)
    elif(t.slice[1].type == 'cadenaS'):
        t[0] = Eprimitivo(t[1],Tipo(5),0)
    elif(t.slice[1].type == 'Rtrue'):
        t[0] = Eprimitivo(1,Tipo(3),0)
    elif(t.slice[1].type == 'Rfalse'):
        t[0] = Eprimitivo(0,Tipo(3),0)
    elif(t.slice[1].type == 'parA'):
        t[0] = t[2]
    elif(t.slice[1].type == 'identificador'):
        t[0] = Eid(t[1],t.lineno(1),find_column(t.lineno(0),t.lexpos(0)))
    elif(t.slice[1].type == 'LLAMADA'):
        t[0] = t[1]

def p_LLAMADA(t):
    '''LLAMADA : identificador parA LPARL parC'''
    t[0] = Llamada(t[1],t[3],t.lineno(0),find_column(t.lineno(0),t.lexpos(0)))

def p_LPARL(t):
    '''LPARL : LPARL coma E
             | E
             | empty'''
    if(t.slice[1].type == "LPARL"):
        t[1].append(t[3])
        t[0] = t[1]
    elif(t.slice[1].type == 'E'):
        t[0] = [t[1]]
    elif(t.slice[1].type == 'empty'):
        t[0] = []

def p_empty(p):
     'empty :'
     pass

def p_error(t):
    print(t)
    lerrores.append(Error("Sintactico","No se esperaba el token: "+t.value,0,0))

from ply import yacc as yacc
parser = yacc.yacc()


def parse(input) :
    global lexer
    global entrada
    entrada = input
    input = input.replace("\r","")
    lexer = lex.lex()
    return parser.parse(input)