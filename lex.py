import ply.lex as lex
from ply.lex import TOKEN


class Lexer(object):
    # List of token names.   This is always required
    tokens = (
        # 'RCURLY_BRACKETS',
        # 'LCURLY_BRACKETS',
        'QUOTE',
        # 'COLON',
        # 'COMMA',
        'NULL',
        'STRING',
        'REAL',
        'INTEGER',
        # 'DOT'
    )

    # Regular expression rules for simple tokens
    # t_LCURLY_BRACKETS = r'{'
    # t_RCURLY_BRACKETS = r'}'
    # t_COLON = r':'
    # t_COMMA = r','
    # t_DOT = r'\.'
    # string = r'({}{}{})'
    quote = r'"'
    text = r'([-_.a-zA-Z])'
    integer = r'([0-9])'

    # string = text
    string = r'({}({}|{})+{})'.format(quote, text, integer, quote)

    # null = r'[n][u][l][l]'
    null = r'null'
    # real = r'([0-9]+)\.'
    # Define a regra para um número real(float) no Sqlite !
    real = r'({}\.{})'.format(integer, integer)

    literals = ['{', '}', ":", ","]

    # def t_lbrace(t):
    #     r'\{'
    #     t.type = '{'      # Set token type to the expected literal
    #     return t

    # def t_rbrace(t):
    #     r'\}'
    #     t.type = '}'      # Set token type to the expected literal
    #     return t
    @TOKEN(null)
    def t_NULL(self, t):
        t.value = None
        return t

    @TOKEN(string)
    def t_STRING(self, t):
        # print(t.value[1:-1])
        t.value = str(t.value[1:-1])
        return t

    @TOKEN(real)
    def t_REAL(self, t):
        # print(t)
        t.value = float(t.value)
        return t

    @TOKEN(integer)
    def t_INTEGER(self, t):
        t.value = int(t.value)
        return t

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    # @TOKEN(number)
    # def t_NUMBER(self,t):
    #     # r'\d+'
    #     t.value = int(t.value)
    #     return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


# Build the lexer and try it out
m = Lexer()
m.build()           # Build the lexer
# m.test('''
# {
#     "id":1,
#     "nome": "Nome",
#     "number": 1,
#     "real": 1.1234,

# }
# ''')     # Test it

# m.test('''
# 1.1234,
# ''')     # Test it

# s = '''{
#         "id":{

#         },


#     }'''

# m.test(s)
