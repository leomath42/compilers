from lex import Lexer
from parser import ParserTable, ParserInsert
import click
import os


class JsonToSQLCompiler:

    def __init__(self, Lexer: Lexer, ParserTable, ParserInsert):
        self.lexer = Lexer()
        self.parser_table = ParserTable(self.lexer)
        self.parser_insert = ParserInsert(self.lexer)

        try:

            self.lexer.build()
            self.parser_table.build()
            self.parser_insert.build()

        except Exception as e:
            print("Exception while building lexer and parsers ")
            raise e

    def __call__(self, string):
        aux = ""

        out = self.parser_table.test(string)
        out = out + "\n\n" if out else ""

        aux += out

        out = self.parser_insert.test(string)
        out = out if out else ""

        aux += out

        return aux


@click.command()
@click.option('--json',
              help='json file to parse.')
@click.option('-o', help='Output file name.')
def _compile(json, o):
    if json is None:
        print("Missing json file !!")
        exit(1)

    compiler = JsonToSQLCompiler(Lexer, ParserTable, ParserInsert)
    try:
        with open(json, 'r') as f:
            text = f.read()
            out = compiler(text)
            if o is not None:
                if not os.path.exists('out'):
                    os.mkdir('out')

                with open('out/'+o, 'w') as f2:
                    f2.write(out)
            else:
                print(out)

    except FileNotFoundError as e:
        print("File not found !")
        raise e
        exit(1)
    except Exception as e:
        print("unexpected exception !")
        raise e
        exit(1)


if __name__ == "__main__":
    _compile()
