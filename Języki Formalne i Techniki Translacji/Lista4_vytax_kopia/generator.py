from utils import *


class Generator:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.labeler = Labeler()

    def generate_const(self, num, reg='a'):
        codes = [Code('RST', reg)]
        if num == 0:
            return codes
        if num == 1:
            return codes + [Code('INC', reg)]
        s = str(bin(num))[2:]
        for char in s[:-1]:
            if char == '1':
                codes += [Code('INC', reg)]
            codes += [Code('SHL', reg)]
        if s[len(s) - 1] == '1':
            codes += [Code('INC', reg)]
        return codes

    def remove_labels(self, codes):
        labels = dict()
        for i in range(len(codes)):
            for label in codes[i].labels:
                if label[1] == '+':
                    labels[label] = i + 1
                else:
                    labels[label] = i
        for code in codes:
            code.labels = []
            if code.arg is not None and str(code.arg)[0] == 'l':
                code.arg = labels[code.arg]

    def generate_all(self, ast):
        proc_code = []
        for procedure in ast[1]:
            proc_code += self.generate_procedure(procedure)

        codes = self.generate_main(ast[2])
        codes += [Code('HALT')]
        codes += proc_code

        self.remove_labels(codes)
        print(self.symbol_table)
        return codes

    def generate_procedure(self, ast):
        proc_head = ast[1]
        proc_name = proc_head[1]
        self.symbol_table.put_procedure(ProcedureData(proc_name, proc_head[2]))
        var_declarations = ast[2]
        for var in var_declarations:
            if type(var) is tuple:
                self.symbol_table.put_array(Array(var[0], var[1]), proc_name)
            else:
                self.symbol_table.put_variable(Variable(var), proc_name)
        commands = ast[3]
        codes = self.generate_from_commands(commands, proc_name)
        codes[0].labels += [f'l_PROC_{proc_name}']

        return_addr = self.symbol_table.get_procedure_parameter_address('RET', proc_name)
        codes += self.generate_const(return_addr, 'a')
        codes += [Code('LOAD', 'a')]
        codes += [Code('JUMPR', 'a')]
        
        return codes

    def generate_main(self, ast):
        var_declarations = ast[1]
        for var in var_declarations:
            if type(var) is tuple:
                self.symbol_table.put_array(Array(var[0], var[1]))
            else:
                self.symbol_table.put_variable(Variable(var))
        commands = ast[2]
        codes = self.generate_from_commands(commands, 'main')
        return codes

    def generate_from_commands(self, commands, proc_name):
        codes = []
        for command in commands:
            if command[0] == 'read':
                codes += self.prepare_identifier_address(command[1], 'b', 'c', True, proc_name)
                codes += [Code('READ'), Code('STORE', 'b')]
            elif command[0] == 'write':
                codes += self.prepare_value(command[1], 'a', 'b', proc_name)
                codes += [Code('WRITE')]
            elif command[0] == 'assign':
                codes += self.calculate_expression(command[2], proc_name)
                move_to_h = False
                if type(command[1]) is tuple and type(
                        command[1][1]) is not int:  # reg a will be overwritten, copy to reg h
                    move_to_h = True
                if proc_name != 'main':
                    if type(command[1]) is tuple:
                        if self.symbol_table.is_param(command[1][0], proc_name) or self.symbol_table.is_param(command[1][1], proc_name):
                            move_to_h = True
                    else:
                        if self.symbol_table.is_param(command[1], proc_name):
                            move_to_h = True
                if move_to_h:
                    codes += [Code('PUT', 'h')]
                codes += self.prepare_identifier_address(command[1], 'b', 'c', True, proc_name)
                if move_to_h:
                    codes += [Code('GET', 'h')]
                codes += [Code('STORE', 'b')]
            elif command[0] == 'if':
                then_commands = self.generate_from_commands(command[2], proc_name)
                label_true = self.labeler.get_label()
                then_commands[0].labels += [label_true]
                label_false = self.labeler.get_label(off_by_one=True)
                then_commands[-1].labels += [label_false]
                codes += self.evaluate_condition(command[1], label_true, label_false, proc_name)
                codes += then_commands
            elif command[0] == 'ifelse':
                then_commands = self.generate_from_commands(command[2], proc_name)
                else_commands = self.generate_from_commands(command[3], proc_name)

                label_true = self.labeler.get_label()
                label_false = self.labeler.get_label()
                label_endif = self.labeler.get_label(off_by_one=True)

                then_commands += [Code('JUMP', label_endif)]
                then_commands[0].labels += [label_true]

                else_commands[0].labels += [label_false]
                else_commands[-1].labels += [label_endif]

                codes += self.evaluate_condition(command[1], label_true, label_false, proc_name)
                codes += then_commands
                codes += else_commands
            elif command[0] == 'while':
                do_commands = self.generate_from_commands(command[2], proc_name)
                label_true = self.labeler.get_label()
                do_commands[0].labels += [label_true]
                label_false = self.labeler.get_label(off_by_one=True)
                cond_code = self.evaluate_condition(command[1], label_true, label_false, proc_name)
                label_loop = self.labeler.get_label()
                cond_code[0].labels += [label_loop]
                do_commands += [Code('JUMP', label_loop)]
                do_commands[-1].labels += [label_false]
                codes += cond_code
                codes += do_commands
            elif command[0] == 'repeat':
                do_commands = self.generate_from_commands(command[1], proc_name)
                label_true = self.labeler.get_label(off_by_one=True)
                label_false = self.labeler.get_label()
                do_commands[0].labels += [label_false]
                cond_code = self.evaluate_condition(command[2], label_true, label_false, proc_name)
                cond_code[-1].labels += [label_true]
                codes += do_commands
                codes += cond_code
            elif command[0] == 'proc_call':
                # reg_a: arg data
                # reg_b: argv pointer
                # reg_c: return address pointer
                # reg_d: return address calculation (ret addr = reg_d + 4)
                procedure = self.symbol_table.get_procedure(command[1], from_func=proc_name)
                if len(procedure.args) != len(command[2]):
                    print(f'BŁĄD: procedura \"{command[1]}\" wymaga {len(procedure.args)} argumentów, a podano {len(command[2])}')
                argv_pointer = procedure.address
                codes += self.generate_const(argv_pointer, 'a')
                codes += [Code('PUT', 'b')]
                codes += [Code('PUT', 'c')]
                for i in range(len(procedure.args)):
                    codes += [Code('INC', 'b')]
                    is_param = False
                    if type(procedure.args[i]) is tuple:
                        if self.symbol_table.is_array(command[2][i], proc_name):
                            addr = self.symbol_table.get_array_address(command[2][i], proc_name)
                        else:
                            addr = self.symbol_table.get_procedure_parameter_address(command[2][i], proc_name)
                            is_param = True
                    else:
                        if self.symbol_table.is_variable(command[2][i], proc_name):
                            #print(f'mak {command[2][i]} {proc_name}')
                            addr = self.symbol_table.get_variable_address(command[2][i], True, proc_name)
                        else:
                            addr = self.symbol_table.get_procedure_parameter_address(command[2][i], proc_name)
                            is_param = True
                    codes += self.generate_const(addr, 'a')
                    if is_param:
                        codes += [Code('LOAD', 'a')]
                    codes += [Code('STORE', 'b')]

                codes += [
                    Code('RST', 'a'),
                    Code('INC', 'a'),
                    Code('SHL', 'a'),
                    Code('SHL', 'a'),

                    Code('STRK', 'd'),
                    Code('ADD', 'd'),
                    Code('STORE', 'c'),
                    Code('JUMP', f'l_PROC_{command[1]}')
                ]
        return codes

    def prepare_value(self, val, target_reg='a', temp_reg='b', proc_name='main'):
        codes = []
        if type(val) is int:
            codes += self.generate_const(val, target_reg)
        else:
            codes += self.prepare_identifier_address(val, target_reg, temp_reg, False, proc_name)
            codes += [Code('LOAD', target_reg)]
            if target_reg != 'a':
                codes += [Code('PUT', target_reg)]
        return codes

    def prepare_identifier_address(self, identifier, target_reg='a', temp_reg='b', write=True, proc_name='main'):
        if proc_name == 'main':
            return self.prepare_identifier_address_main(identifier, target_reg, temp_reg, write)

        codes = []
        if type(identifier) is tuple:
            if type(identifier[1]) is int:  # pidentifier[num]
                if self.symbol_table.is_array(identifier[0], proc_name):
                    adr = self.symbol_table.get_array_element_adr_const(identifier[0], identifier[1], write, proc_name)
                    codes += self.generate_const(adr, target_reg)
                else:
                    adr = self.symbol_table.get_procedure_parameter_address(identifier[0], proc_name)
                    codes += self.generate_const(adr, temp_reg)
                    codes += [Code('LOAD', temp_reg)]
                    codes += self.generate_const(identifier[1], temp_reg)
                    codes += [Code('ADD', temp_reg)]
                    if target_reg != 'a':
                        codes += [Code('PUT', target_reg)]
            else:  # pidentifier[pidentifier]
                if self.symbol_table.is_array(identifier[0], proc_name) and self.symbol_table.is_variable(identifier[1], proc_name):
                    # variable[variable]
                    array_addr = self.symbol_table.get_array_address(identifier[0], proc_name)
                    index_var_addr = self.symbol_table.get_variable_address(identifier[1], False, proc_name)
                    codes += self.generate_const(index_var_addr, temp_reg)
                    codes += [Code('LOAD', temp_reg)]
                    codes += self.generate_const(array_addr, temp_reg)
                    codes += [Code('ADD', temp_reg)]
                    if target_reg != 'a':
                        codes += [Code('PUT', target_reg)]
                elif self.symbol_table.is_array(identifier[0], proc_name) and (not self.symbol_table.is_variable(identifier[1], proc_name)):
                    # variable[parameter]
                    array_addr = self.symbol_table.get_array_address(identifier[0], proc_name)
                    index_var_addr = self.symbol_table.get_procedure_parameter_address(identifier[1], proc_name)
                    codes += self.generate_const(index_var_addr, temp_reg)
                    codes += [Code('LOAD', temp_reg)]
                    codes += [Code('LOAD', 'a')]
                    codes += self.generate_const(array_addr, temp_reg)
                    codes += [Code('ADD', temp_reg)]
                    if target_reg != 'a':
                        codes += [Code('PUT', target_reg)]
                elif (not self.symbol_table.is_array(identifier[0], proc_name)) and self.symbol_table.is_variable(identifier[1], proc_name):
                    # parameter[variable]
                    array_addr = self.symbol_table.get_procedure_parameter_address(identifier[0], proc_name)
                    index_var_addr = self.symbol_table.get_variable_address(identifier[1], False, proc_name)
                    codes += self.generate_const(index_var_addr, temp_reg)
                    codes += [Code('LOAD', temp_reg)]
                    codes += [Code('PUT', temp_reg)]
                    codes += self.generate_const(array_addr, target_reg)
                    codes += [Code('LOAD', target_reg)]
                    codes += [Code('ADD', temp_reg)]
                    if target_reg != 'a':
                        codes += [Code('PUT', target_reg)]
                else:
                    # parameter[parameter]
                    array_addr = self.symbol_table.get_procedure_parameter_address(identifier[0], proc_name)
                    index_var_addr = self.symbol_table.get_procedure_parameter_address(identifier[1], proc_name)
                    codes += self.generate_const(index_var_addr, temp_reg)
                    codes += [Code('LOAD', temp_reg)]
                    codes += [Code('LOAD', 'a')]
                    codes += [Code('PUT', temp_reg)]
                    codes += self.generate_const(array_addr, target_reg)
                    codes += [Code('LOAD', target_reg)]
                    codes += [Code('ADD', temp_reg)]
                    if target_reg != 'a':
                        codes += [Code('PUT', target_reg)]

        else:  # pidentifier
            if self.symbol_table.is_variable(identifier, proc_name):
                var_addr = self.symbol_table.get_variable_address(identifier, write, proc_name)
                codes += self.generate_const(var_addr, target_reg)
            else:
                var_addr = self.symbol_table.get_procedure_parameter_address(identifier, proc_name)
                codes += self.generate_const(var_addr, temp_reg)
                codes += [Code('LOAD', temp_reg)]
                if target_reg != 'a':
                    codes += [Code('PUT', target_reg)]

        return codes

    def prepare_identifier_address_main(self, identifier, target_reg='a', temp_reg='b', write=True):
        codes = []
        if type(identifier) is tuple:
            if type(identifier[1]) is int:  # pidentifier[num]
                adr = self.symbol_table.get_array_element_adr_const(identifier[0], identifier[1], write, 'main')
                codes += self.generate_const(adr, target_reg)
            else:  # pidentifier[pidentifier]
                array_addr = self.symbol_table.get_array_address(identifier[0], 'main')
                index_var_addr = self.symbol_table.get_variable_address(identifier[1], False, 'main')
                codes += self.generate_const(index_var_addr, temp_reg)
                codes += [Code('LOAD', temp_reg)]
                codes += self.generate_const(array_addr, temp_reg)
                codes += [Code('ADD', temp_reg)]
                if target_reg != 'a':
                    codes += [Code('PUT', target_reg)]
        else:  # pidentifier
            var_addr = self.symbol_table.get_variable_address(identifier, write, 'main')
            codes += self.generate_const(var_addr, target_reg)
        return codes

    def calculate_expression(self, expr, proc_name='main'):
        codes = []
        if expr[0] == 'val':
            codes += self.prepare_value(expr[1], target_reg='a', temp_reg='b', proc_name=proc_name)
        elif expr[0] == '+':
            codes += self.prepare_value(expr[1], target_reg='c', temp_reg='b', proc_name=proc_name)
            codes += self.prepare_value(expr[2], target_reg='a', temp_reg='b', proc_name=proc_name)
            codes += [Code('ADD', 'c')]
        elif expr[0] == '-':
            codes += self.prepare_value(expr[2], target_reg='c', temp_reg='b', proc_name=proc_name)
            codes += self.prepare_value(expr[1], target_reg='a', temp_reg='b', proc_name=proc_name)
            codes += [Code('SUB', 'c')]
        elif expr[0] == '*':
            label_skip = self.labeler.get_label(off_by_one=True)
            codes += self.prepare_value(expr[2], target_reg='a', temp_reg='c', proc_name=proc_name)
            codes += [Code('JZERO', label_skip),
                      Code('PUT', 'b')]
            codes += self.prepare_value(expr[1], target_reg='a', temp_reg='c', proc_name=proc_name)
            codes += [Code('JZERO', label_skip),
                      Code('PUT', 'c')]

            label_loop = self.labeler.get_label()
            label_even = self.labeler.get_label()

            # input: a * b
            #
            # reg_b : b
            # reg_c : a
            # reg_d : result

            codes += [
                # result := 0
                Code('RST', 'd'),

                # loop: if a % 2 > 0:
                Code('SHR', 'c', [label_loop]),
                Code('SHL', 'c'),
                Code('SUB', 'c'),
                Code('JZERO', label_even),

                # then: result := result + b
                Code('GET', 'd'),
                Code('ADD', 'b'),
                Code('PUT', 'd'),

                # endif
                # b := b * 2; a := a / 2
                Code('SHL', 'b', [label_even]),
                Code('SHR', 'c'),

                # if a > 0 goto loop
                Code('GET', 'c'),
                Code('JPOS', label_loop),

                # return result
                Code('GET', 'd', [label_skip]),
            ]
        elif expr[0] == '/' or expr[0] == '%':
            label_skip = self.labeler.get_label(off_by_one=True)
            codes += self.prepare_value(expr[2], target_reg='a', temp_reg='c', proc_name=proc_name)
            codes += [Code('JZERO', label_skip),
                      Code('PUT', 'b')]
            codes += self.prepare_value(expr[1], target_reg='a', temp_reg='c', proc_name=proc_name)
            codes += [Code('JZERO', label_skip)]

            label_begin = self.labeler.get_label()
            label_loop = self.labeler.get_label()
            label_end = self.labeler.get_label()
            label_shl_enter = self.labeler.get_label()
            label_shl_exit = self.labeler.get_label()

            # input: a / b or a % b
            #
            # reg_b : b
            # reg_c : k
            # reg_d : q
            # reg_e : quotient (result of /)
            # reg_f : a (result of %)

            codes += [
                # quotient := 0
                Code('RST', 'e'),

                Code('JUMP', label_begin),

                # a := a - k
                Code('SUB', 'c', [label_loop]),
                Code('PUT', 'f', [label_begin]),

                # loop: if a < b goto end
                Code('GET', 'b'),
                Code('SUB', 'f'),
                Code('JPOS', label_end),

                # k := b
                Code('GET', 'b'),
                Code('PUT', 'c'),

                # q := 1
                Code('RST', 'd'),
                Code('INC', 'd'),

                # x: k := k * 2
                # if k < a then q := q * 2 and goto x
                Code('GET', 'f', [label_shl_exit]),
                Code('SHL', 'c'),
                Code('SUB', 'c'),
                Code('JPOS', label_shl_enter),

                # k := k / 2
                Code('SHR', 'c'),

                # quotient := quotient + q
                Code('GET', 'e'),
                Code('ADD', 'd'),
                Code('PUT', 'e'),

                # goto loop
                Code('GET', 'f'),
                Code('JUMP', label_loop),

                # q := q * 2 routine
                Code('SHL', 'd', [label_shl_enter]),
                Code('JUMP', label_shl_exit),
            ]

            # end (return result)
            if expr[0] == '/':
                codes += [Code('GET', 'e', [label_end, label_skip])]
            else:
                codes += [Code('GET', 'f', [label_end, label_skip])]

        return codes

    def evaluate_condition(self, cond, label_true, label_false, proc_name='main'):
        codes = []
        if cond[0] == 'eq':
            codes += self.prepare_value(cond[2], target_reg='c', temp_reg='b', proc_name=proc_name)
            codes += self.prepare_value(cond[1], target_reg='a', temp_reg='b', proc_name=proc_name)
            codes += [Code('PUT', 'd')]
            codes += [Code('SUB', 'c')]
            codes += [Code('JPOS', label_false)]
            codes += [Code('GET', 'c')]
            codes += [Code('SUB', 'd')]
            codes += [Code('JPOS', label_false)]
        elif cond[0] == 'neq':
            codes += self.prepare_value(cond[2], target_reg='c', temp_reg='b', proc_name=proc_name)
            codes += self.prepare_value(cond[1], target_reg='a', temp_reg='b', proc_name=proc_name)
            codes += [Code('PUT', 'd')]
            codes += [Code('SUB', 'c')]
            codes += [Code('JPOS', label_true)]
            codes += [Code('GET', 'c')]
            codes += [Code('SUB', 'd')]
            codes += [Code('JPOS', label_true)]
            codes += [Code('JUMP', label_false)]
        elif cond[0] == 'gt':
            codes += self.prepare_value(cond[2], target_reg='c', temp_reg='b', proc_name=proc_name)
            codes += self.prepare_value(cond[1], target_reg='a', temp_reg='b', proc_name=proc_name)
            codes += [Code('SUB', 'c')]
            # codes += [Code('JPOS', label_true), Code('JUMP', label_false)]
            codes += [Code('JZERO', label_false)]
        elif cond[0] == 'lt':
            codes += self.prepare_value(cond[1], target_reg='c', temp_reg='b', proc_name=proc_name)
            codes += self.prepare_value(cond[2], target_reg='a', temp_reg='b', proc_name=proc_name)
            codes += [Code('SUB', 'c')]
            # codes += [Code('JPOS', label_true), Code('JUMP', label_false)]
            codes += [Code('JZERO', label_false)]
        elif cond[0] == 'ge':
            codes += self.prepare_value(cond[1], target_reg='c', temp_reg='b', proc_name=proc_name)
            codes += self.prepare_value(cond[2], target_reg='a', temp_reg='b', proc_name=proc_name)
            codes += [Code('SUB', 'c')]
            codes += [Code('JPOS', label_false)]
        elif cond[0] == 'le':
            codes += self.prepare_value(cond[2], target_reg='c', temp_reg='b', proc_name=proc_name)
            codes += self.prepare_value(cond[1], target_reg='a', temp_reg='b', proc_name=proc_name)
            codes += [Code('SUB', 'c')]
            codes += [Code('JPOS', label_false)]
        return codes
