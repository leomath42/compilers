import ply.yacc as yacc
from lex import Lexer


class ParserTable(object):
    tokens = Lexer.tokens
    # lexer = Lexer()

    def __init__(self, lexer: Lexer, table_name='table'):
        self.lexer = Lexer()
        self.table_name = table_name

    def p_start(self, p):
        '''S : '[' objects ']'
             | '['  ']'
             | object
        '''

        if len(p) == 4:
            # retorna uma lista com as tabelas criadas no caso de ser um array de objects::
            if isinstance(p[2], list):
                aux = '\n'.join(p[2])
                p[0] = aux
            else:
                p[0] = p[2]
            # # Retorna somente o primeiro item da lista de objects.
            # p[0] = p[2][0]
        elif len(p) == 2:
            p[0] = p[1]

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
        p[1] = 'CREATE TABLE {}('.format(self.table_name)
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
              | K ':' S
        '''

        p[2] = ''

        if p[3].startswith('CREATE'):
            # Tabela aninhadas
            aux = p[3]
            aux = aux.replace('table', '{}_table'.format(p[1]))

            p[3] = "INTEGER REFERENCES {}_table".format(p[1])

        p[0] = "{} {} {}".format(p[1], p[2], p[3])

    def p_key_string(self, p):
        'K : STRING'
        p[0] = p[1]

    def p_value_expression(self, p):
        '''V  : V1 ',' E
              | V1
        '''

        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 4:
            p[0] = "{}{} {}".format(p[1], p[2], p[3])
        else:
            raise Exception('Error::')

    def p_value_terminals(self, p):
        '''V1   : STRING
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

    def test(self, data,  table_name='table'):
        # self.lexer.input(data)
        self.table_name = table_name
        return self.parser.parse(data)


class ParserInsert(object):
    tokens = Lexer.tokens
    # lexer = Lexer()

    # tables = {}

    def __init__(self, lexer: Lexer, table_name='table'):
        self.lexer = Lexer()
        self.table_name = table_name
        self.table_fg_count = 1

    def p_start_insert(self, p):
        '''S : '[' objects ']'
             | '['  ']'
             | objects
        '''

        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]
        elif len(p) == 3:
            p[0] = ''

    def p_objects_array_insert(self, p):
        '''
        objects : object
                | object ',' objects
        '''

        if p[1] is None:
            p[0] = 'null'
        elif len(p) == 2 and p[1] is not None:
            p[0] = "INSERT INTO {}{} values{};".format(
                self.table_name, p[1][0], p[1][1])
        elif len(p) == 4:
            p[0] = "INSERT INTO {}{} values{};".format(
                self.table_name, p[1][0], p[1][1]) + '\n' + p[3]

    def p_curly_expression_insert(self, p):
        '''object : '{' E '}' '''

        if p[2] is not None:
            p[0] = p[2]

            aux = p[0].split('|')

            if len(aux) % 2:
                raise SyntaxError("error")
            else:
                names = "("
                values = "("

                for i in range(0, len(aux)-2, 2):
                    names += aux[i] + ", "
                    if not aux[i+1].startswith('INSERT'):
                        values += aux[i+1] + ", "
                    else:
                        _ = aux[i].replace('table',
                                           '{}_table'.format(aux[i+1])) + ")"
                        # print(_)
                names += aux[len(aux)-2] + ")"
                if not aux[len(aux)-1].startswith('INSERT'):
                    values += aux[len(aux)-1] + ")"
                else:
                    _ = aux[len(aux)-1].replace('table',
                                                '{}_table'.format(aux[len(aux)-2])) + ")"
                    # print(_)
                    values += str(self.table_fg_count) + ")"
                    self.table_fg_count += 1

            p[0] = (names, values)

    def p_e_expression_insert(self, p):
        '''E : E1
             |
        '''

        if len(p) == 2:
            p[0] = p[1]

    def p_E_key_colon_value_expression_insert(self, p):
        '''E1 : K ':' V
              | K ':' S
        '''

        p[0] = "{}{}{}".format(p[1], "|", p[3])

    def p_key_string_insert(self, p):
        'K : STRING'
        p[0] = p[1]

    def p_value_expression_insert(self, p):
        '''V  : V1 ',' E
              | V1
        '''

        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = "{}{}{}".format(p[1], "|", p[3])

    def p_value_terminals_insert(self, p):
        '''V1   : STRING
                | REAL
                | INTEGER
                | NULL
        '''
        if p[1] is None:
            p[1] = 'null'
        elif isinstance(p[1], str):
            p[1] = '\'' + p[1] + '\''

        p[0] = p[1]

    def p_error(self, p):
        print(p)
        print("Syntax error in input!")

    def build(self, **kwargs):
        # self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)

    def test(self, data, table_name="table"):
        self.table_name = table_name
        return self.parser.parse(data)


if __name__ == "__main__":
    lexer = Lexer()
    lexer.build()
    p = ParserTable(lexer)
    p.build()
    out = p.test('''
    {
        "id":1,
        "nome": "Nome",
        "number": "100-5..-_",
        "real": 1.1234

    }
    ''')

    print(out)
