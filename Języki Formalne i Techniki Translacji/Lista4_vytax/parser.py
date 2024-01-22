from sly import Parser
from lexer import MyLexer
from generator import Generator


class MyParser(Parser):
    tokens = MyLexer.tokens

    @_('procedures main')
    def program_all(self, p):
        return ('program_all', p.procedures, p.main)

    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, p):
        return p.procedures + [('procedure', p.proc_head, p.declarations, p.commands)]

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):
        return p.procedures + [('procedure', p.proc_head, [], p.commands)]

    @_('')
    def procedures(self, p):
        return []

    @_('PROGRAM IS declarations IN commands END')
    def main(self, p):
        return ('main', p.declarations, p.commands)

    @_('PROGRAM IS IN commands END')
    def main(self, p):
        return ('main', [], p.commands)

    @_('commands command')
    def commands(self, p):
        return p.commands + [p.command]

    @_('command')
    def commands(self, p):
        return [p.command]

    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        return ('assign', p.identifier, p.expression)

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return ('ifelse', p.condition, p.commands0, p.commands1)

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return ('if', p.condition, p.commands)

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return ('while', p.condition, p.commands)

    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        return ('repeat', p.commands, p.condition)

    @_('proc_call ";"')
    def command(self, p):
        return p.proc_call

    @_('READ identifier ";"')
    def command(self, p):
        return ('read', p.identifier)

    @_('WRITE value ";"')
    def command(self, p):
        return ('write', p.value)

    @_('PIDENTIFIER "(" args_decl ")"')
    def proc_head(self, p):
        return ('proc_head', p.PIDENTIFIER, p.args_decl)

    @_('PIDENTIFIER "(" args ")"')
    def proc_call(self, p):
        return ('proc_call', p.PIDENTIFIER, p.args)

    @_('declarations "," PIDENTIFIER')
    def declarations(self, p):
        return p.declarations + [p.PIDENTIFIER]

    @_('declarations "," PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        return p.declarations + [(p.PIDENTIFIER, p.NUM)]

    @_('PIDENTIFIER')
    def declarations(self, p):
        return [p.PIDENTIFIER]

    @_('PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        return [(p.PIDENTIFIER, p.NUM)]

    @_('args_decl "," PIDENTIFIER')
    def args_decl(self, p):
        return p.args_decl + [p.PIDENTIFIER]

    @_('args_decl "," "T" PIDENTIFIER')
    def args_decl(self, p):
        return p.args_decl + [('T', p.PIDENTIFIER)]

    @_('PIDENTIFIER')
    def args_decl(self, p):
        return [p.PIDENTIFIER]

    @_('"T" PIDENTIFIER')
    def args_decl(self, p):
        return [('T', p.PIDENTIFIER)]

    @_('args "," PIDENTIFIER')
    def args(self, p):
        return p.args + [p.PIDENTIFIER]

    @_('PIDENTIFIER')
    def args(self, p):
        return [p.PIDENTIFIER]

    @_('value')
    def expression(self, p):
        return ('val', p.value)

    @_('value "+" value')
    def expression(self, p):
        return ('+', p.value0, p.value1)

    @_('value "-" value')
    def expression(self, p):
        return ('-', p.value0, p.value1)

    @_('value "*" value')
    def expression(self, p):
        return ('*', p.value0, p.value1)

    @_('value "/" value')
    def expression(self, p):
        return ('/', p.value0, p.value1)

    @_('value "%" value')
    def expression(self, p):
        return ('%', p.value0, p.value1)

    @_('value EQ value')
    def condition(self, p):
        return ('eq', p.value0, p.value1)

    @_('value NEQ value')
    def condition(self, p):
        return ('neq', p.value0, p.value1)

    @_('value GT value')
    def condition(self, p):
        return ('gt', p.value0, p.value1)

    @_('value LT value')
    def condition(self, p):
        return ('lt', p.value0, p.value1)

    @_('value GE value')
    def condition(self, p):
        return ('ge', p.value0, p.value1)

    @_('value LE value')
    def condition(self, p):
        return ('le', p.value0, p.value1)

    @_('NUM')
    def value(self, p):
        return p.NUM

    @_('identifier')
    def value(self, p):
        return p.identifier

    @_('PIDENTIFIER')
    def identifier(self, p):
        return p.PIDENTIFIER

    @_('PIDENTIFIER "[" NUM "]"')
    def identifier(self, p):
        return (p.PIDENTIFIER, p.NUM)

    @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    def identifier(self, p):
        return (p.PIDENTIFIER0, p.PIDENTIFIER1)

    def error(self, p):
        print(f'BŁĄD: błąd parsowania (\"{p.value}\" w linii {p.lineno})')
        exit(3)
