import ply.yacc as yacc
from lex import Lexer

tokens = Lexer.tokens

'''
tokens = (
    'RCURLY_BRACKETS',
    'LCURLY_BRACKETS',
    'QUOTE',
    'COLON',
    'COMMA',
    'STRING',
    'REAL',
    'INTEGER',
    # 'NULL'
    # 'DOT'
)
{
 "id":1,
 "nome": "Nome",
 "number": 1,
 "real": 1.1234, 
}

CREATE TABLE table( : LCURLY_BRACKETS
)                   : RCURLY_BRACKETS

LCURLY_BRACKETS exp  COLON


# S : LCURLY_BRACKETS

# term : LCURLY_BRACKETS STRING

# term: RCURLY_BRACKETS


S : LCURLY_BRACKETS E
E: STRING E

term: STRING

CREATE TABLE table(
    id INTEGER,
    nome TEXT,
    number INTEGER,
    real REAL
)


--

S => { E }
E => K:V
K => string
V => V1 | V1,S
V1 => string| real | integer | null
--


'''

# def p_start(p):
#     'S : LCURLY_BRACKETS'
#     print(list(p))


def p_curly_expression(p):
    '''S : '{' E '}' '''
    p[1] = 'CREATE TABLE table('
    p[3] = ');'

    p[0] = "{} {} {}".format(p[1], p[2], p[3])


def p_e_expression(p):
    '''E : E1
         | '''

    if len(p) == 1 and p[0] is None:
        p[0] = ""
    else:
        p[0] = p[1]


def p_E_key_colon_value_expression(p):
    '''E1 : K ':' V
          | K ':' S '''

    p[2] = ''

    if p[3].startswith('CREATE'):
        aux = p[3]
        print('foi')
        aux = aux.replace('table', '{}_table'.format(p[1]))

        p[3] = "INTEGER REFERENCES {}_table".format(p[1])

        print(aux)

    p[0] = "{} {} {}".format(p[1], p[2], p[3])


def p_key_string(p):
    'K : STRING'
    p[0] = p[1]


def p_value_expression(p):
    '''V : V1 ',' E
         | V1'''

    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 4:
        p[0] = "{}{} {}".format(p[1], p[2], p[3])
    else:
        print('errorrrrrrrrrrr')
        # raise Exception('Error::')


def p_value_terminals(p):
    '''V1 : STRING
          | REAL
          | INTEGER
          | NULL
    '''

    if(isinstance(p[1], str)):
        p[0] = 'TEXT'
    elif (isinstance(p[1], int)):
        p[0] = 'INTEGER'
    elif (isinstance(p[1], float)):
        p[0] = 'REAL'
    elif p[1] is None:
        # ao criar uma tabela, converte o valor para TEXT
        p[0] = 'TEXT'
    else:
        print('errorrrrrrrrrrr')
        # raise Exception('ERROR::')

    print(list(p))


# def p_5(p):
#     'VALUE : INTEGER'
#     # print('called')
#     print(list(p))
#     p[0] = 'INTEGER'

# def p_expression_plus(p):
#     'term : LCURLY_BRACKETS'
#     print(list(p))
#     p[0] = p[1] + p[3]

# Error rule for syntax errors


def p_error(p):
    print(p)
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

# while True:
#    try:
#        s = input('teste > ')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print(result)

# s = '''{"id":5}'''
# s = '''{"id":5}'''
s = '''{
        "id":{"x":5}
    }'''
result = parser.parse(s)
print(result)
