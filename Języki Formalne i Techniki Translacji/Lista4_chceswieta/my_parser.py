from my_lexer import MyLexer
from sly import Parser

class MyParser(Parser):
    tokens = MyLexer.tokens     
    
    # program_all ---------------------------------------------------
    @_('procedures main',)
    def program_all(self, p):
        return ('program_all', p.procedures, p.main)

    # procedures ----------------------------------------------------
    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, p):
        return p.procedures + [('procedure', p.proc_head, p.declarations, p.commands)]

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):
        return p.procedures + [('procedure', p.proc_head, [], p.commands)]

    @_('')
    def procedures(self, p):
        return []

    # main ----------------------------------------------------------
    @_('PROGRAM IS declarations IN commands END')
    def main(self, p):
        return ('main', p.declarations, p.commands)
    
    @_('PROGRAM IS IN commands END')
    def main(self, p):
        return ('main', [], p.commands)

    # commands ------------------------------------------------------
    @_('commands command')
    def commands(self, p):
        return p[0] + [p[1]]

    @_('command')
    def commands(self, p):
        return [p[0]]

    # command -------------------------------------------------------
    @_('proc_call')
    def command(self, p):
        return p.proc_call

    @_('REPEAT commands UNTIL condition')
    def command(self, p):
        return ('repeat', p.commands, p.condition)

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return ('while', p.condition, p.commands)

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return ('ifelse', p.condition, p.commands0, p.commands1)

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return ('if', p.condition, p.commands)

    @_('WRITE value')
    def command(self, p):
        return ('write', p.value)

    @_('READ identifier')
    def command(self, p):
        return ('read', p.identifier)
    
    @_('identifier ASS expression')
    def command(self, p):
        return ('assign', p.identifier, p.expression)

    # proc_head -----------------------------------------------------
    @_('PIDENTIFIER LPAREN args_decl RPAREN')
    def proc_head(self, p):
        return ('proc_head', p.PIDENTIFIER, p.args_decl)

    # proc_call -----------------------------------------------------
    @_('PIDENTIFIER LPAREN args RPAREN')
    def proc_call(self, p):
        return ('proc_call', p.PIDENTIFIER, p.args)
        

    # declarations --------------------------------------------------
    @_('declarations COMA PIDENTIFIER',
       'PIDENTIFIER')
    def declarations(self, p):
        if len(p) == 3:
            return p.declarations + [p.PIDENTIFIER]
        else:
            return [p.PIDENTIFIER]
        

    @_('declarations COMA PIDENTIFIER LBRACK NUM RBRACK',
       'PIDENTIFIER LBRACK NUM RBRACK')
    def declarations(self, p):
        if len(p) == 6:
            return p.declarations + [(p.PIDENTIFIER, p.NUM)]
        else:
            return [(p.PIDENTIFIER, p.NUM)]

    # args_decl -----------------------------------------------------
    @_('args_decl COMA PIDENTIFIER',
       'PIDENTIFIER')
    def args_decl(self, p):
        if len(p) == 3:
            return p.args_decl + [p.PIDENTIFIER]
        else:
            return [p.PIDENTIFIER]

    @_('args_decl COMA T PIDENTIFIER',
       'T PIDENTIFIER')
    def args_decl(self, p):
        if len(p) == 4:
            return p.args_decl + [('T', p.PIDENTIFIER)]
        else:
            return [('T', p.PIDENTIFIER)]

    # args ----------------------------------------------------------
    @_('args COMA PIDENTIFIER')
    def args(self, p):
        return p.args + [p.PIDENTIFIER]

    @_('PIDENTIFIER')
    def args(self, p):
        return [p.PIDENTIFIER]

    # expression ----------------------------------------------------
    @_('value ADD value',
       'value SUB value',
       'value MUL value',
       'value DIV value',
       'value MOD value')
    def expression(self, p):
        return p[1], p[0], p[2]

    @_('value')
    def expression(self, p):
        return ('val', p.value)

    # condition -----------------------------------------------------
    @_('value EQ value',
       'value NEQ value',
       'value GT value',
       'value LT value',
       'value GEQ value',
       'value LEQ value')
    def condition(self, p):
        return (p[1], p.value0, p.value1)

    # value ---------------------------------------------------------
    @_('NUM',
       'identifier')
    def value(self, p):
        return p[0]

    # identifier ----------------------------------------------------
    @_('PIDENTIFIER')
    def identifier(self, p):
        return p.PIDENTIFIER

    @_('PIDENTIFIER LBRACK NUM RBRACK',
       'PIDENTIFIER LBRACK PIDENTIFIER RBRACK')
    def identifier(self, p):
        return (p.PIDENTIFIER + p[2])