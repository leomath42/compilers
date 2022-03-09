import ply.yacc as yacc
from lex import Lexer

# tokens = Lexer.tokens

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


class ParserTable(object):
    tokens = Lexer.tokens
    # lexer = Lexer()

    def __init__(self, lexer: Lexer):
        self.lexer = Lexer()

    def p_start(self, p):
        '''S : '[' objects ']'
            | '['  ']'
        '''
        if(len(p) == 4):
            # retorna uma lista com as tabelas criadas no caso de ser um array de objects::
            aux = '\n'.join(p[2])
            p[0] = aux

            # # Retorna somente o primeiro item da lista de objects.
            # p[0] = p[2][0]

        else:
            p[0] = ''

    def p_objects_array(self, p):
        '''
        objects : object
                | object ',' objects
        '''
        if(len(p) == 2):
            p[0] = p[1]
        else:
            p[0] = [p[1], p[3]]

    def p_curly_expression(self, p):
        '''object : '{' E '}' '''
        p[1] = 'CREATE TABLE table('
        p[3] = ');'

        p[0] = "{} {} {}".format(p[1], p[2], p[3])

    def p_e_expression(self, p):
        '''E : E1
            | '''

        if len(p) == 1 and p[0] is None:
            p[0] = ""
        else:
            p[0] = p[1]

    def p_E_key_colon_value_expression(self, p):
        '''E1 : K ':' V
            | K ':' S '''

        p[2] = ''

        if p[3].startswith('CREATE'):
            aux = p[3]
            aux = aux.replace('table', '{}_table'.format(p[1]))

            p[3] = "INTEGER REFERENCES {}_table".format(p[1])

        p[0] = "{} {} {}".format(p[1], p[2], p[3])

    def p_key_string(self, p):
        'K : STRING'
        p[0] = p[1]

    def p_value_expression(self, p):
        '''V : V1 ',' E
            | V1'''

        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 4:
            p[0] = "{}{} {}".format(p[1], p[2], p[3])
        else:
            raise Exception('Error::')

    def p_value_terminals(self, p):
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
            raise Exception('ERROR::')

    def p_error(self, p):
        print(p)
        print("Syntax error in input!")

    def build(self, **kwargs):
        # self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    def test(self, data):
        # self.lexer.input(data)
        return self.parser.parse(data)


class ParserInsert(object):
    tokens = Lexer.tokens
    # lexer = Lexer()

    def __init__(self, lexer: Lexer):
        self.lexer = Lexer()

    def p_start(self, p):
        '''S : '[' objects ']'
            | '['  ']'
        '''
        ...

    def p_error(self, p):
        print(p)
        print("Syntax error in input!")

    def build(self, **kwargs):
        # self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    def test(self, data):
        # self.lexer.input(data)
        return self.parser.parse(data)


if __name__ == "__main__":
    lexer = Lexer()
    lexer.build()

    # p = ParserTable(lexer)
    p = ParserInsert(lexer)
    s = '''[ {"id": 5}, {"idpk" : 0}]'''

    p.build()
    print(p.test(s))
    # p2.build()
    # print(p2.test(s))
