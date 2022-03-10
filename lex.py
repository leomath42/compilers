import ply.lex as lex
from ply.lex import TOKEN


class Lexer(object):
    # List of token names.
    tokens = (
        'NULL',
        'REAL',
        'STRING',
        'INTEGER'
    )

    # Regular expression rules
    quote = r'"'
    text = r'([-_.a-zA-Z]|[éáíóúãõũẽãç]|[ÉÁÍÓÚÃÕŨẼÃÇ])'
    digit = r'([0-9])'
    integer = r'([0-9])+'

    string = r'({}({}|{})+{})'.format(quote, text, integer, quote)

    null = r'null'
    # Define a regra para um número real(float) no Sqlite !
    real = r'({}\.{})'.format(integer, integer)

    literals = ['{', '}', ":", ",", "[", "]"]

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

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

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


if __name__ == "__main__":
    # Build the lexer
    m = Lexer()
    m.build()
    out = m.test('''
    {
        "id":1,
        "nome": "Nome",
        "number": "100-5..-_",
        "real": 1.1234

    }
    ''')
    print(out)
