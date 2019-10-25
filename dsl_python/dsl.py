from sly import Lexer, Parser
from werkzeug import exceptions


class CalcLexer(Lexer):
    tokens = {NUMBER}
    ignore = ' \t\n'
    literals = {'+'}

    @_(r'\d+(\.\d+)?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    def error(self, t):
        raise exceptions.BadRequest(f"Illegal sequence '{t.value}'")


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    def error(self, p):
        if p is None:
            raise exceptions.BadRequest("Syntax error, unexpected EOF")
        raise exceptions.BadRequest(
            f"Syntax error near '{p.value}', line={p.lineno} column={p.index}")

    @_('operation')
    def statement(self, p):
        return p.operation

    @_('NUMBER')
    def operation(self, p):
        return p.NUMBER

    @_('NUMBER "+" NUMBER')
    def operation(self, p):
        return p.NUMBER0 + p.NUMBER1