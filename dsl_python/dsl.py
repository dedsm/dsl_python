import operator

from sly import Lexer, Parser
from werkzeug import exceptions


class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, DIVIDE, TIMES}
    ignore = ' \t\n'
    literals = {'(', ')'}

    @_(r'\d+(\.\d+)?')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'\+')
    def PLUS(self, t):
        t.value = operator.add
        return t

    @_(r'-')
    def MINUS(self, t):
        t.value = operator.sub
        return t

    @_(r'/')
    def DIVIDE(self, t):
        t.value = operator.truediv
        return t

    @_(r'\*')
    def TIMES(self, t):
        t.value = operator.mul
        return t

    def error(self, t):
        raise exceptions.BadRequest(f"Illegal sequence '{t.value}'")


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', DIVIDE, TIMES),
    )

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

    @_('"(" operation ")"')
    def operation(self, p):
        return p.operation

    @_(
        'operation PLUS operation',
        'operation MINUS operation',
        'operation TIMES operation',
        'operation DIVIDE operation',
    )
    def operation(self, p):
        return p[1](p.operation0, p.operation1)
