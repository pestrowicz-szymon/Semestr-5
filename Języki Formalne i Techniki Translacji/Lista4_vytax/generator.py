from my_array import Array
from my_code import Code
from my_labeler import Labeler
from my_procedure_data import ProcedureData
from my_symbol_table import SymbolTable, DataType
from my_variable import Variable

class Generator:
    def __init__(self):
        self.symbols = SymbolTable()
        self.labeler = Labeler()

    def compile_all(self, parser_result):
        procedures_result = []
        for procedure in parser_result[1]:
            procedures_result += self.compile_procedure(procedure)

        main_result = self.compile_main(parser_result[2])
        main_result[0].labels += ['label_main']

        assembly_code = [Code('JUMP', 'label_main')]
        assembly_code += procedures_result
        assembly_code += main_result
        assembly_code += [Code('HALT')]

        #remove labels from jump function
        labels = dict()
        for i in range(len(assembly_code)):
            for label in assembly_code[i].labels:
                if label[1] == '-':
                    labels[label] = i + 1
                else:
                    labels[label] = i
        for code in assembly_code:
            code.labels = []
            if code.arg is not None and str(code.arg)[0] == 'l':
                code.arg = labels[code.arg]

        return assembly_code

    def compile_procedure(self, procedure):
        proc_head = procedure[1]
        proc_name = proc_head[1]
        self.symbols.put(ProcedureData(proc_name, proc_head[2]), DataType.PROCEDURE)
        var_declarations = procedure[2]
        for var in var_declarations:
            if var[0] == 'T':
                self.symbols.put(Array(var[0], var[1]), DataType.ARRAY, proc_name)
            else:
                self.symbols.put(Variable(var), DataType.VARIABLE,proc_name)
        commands = procedure[3]
        assembly_code = self.generate_from_commands(commands, proc_name)
        assembly_code[0].labels += [f'l_PROCEDURE_{proc_name}']

        return_addr = self.symbols.get_procedure_parameter_address('RET', proc_name)
        assembly_code += self.generate_value(return_addr, 'a')
        assembly_code += [Code('LOAD', 'a')]
        assembly_code += [Code('JUMPR', 'a')]
        
        return assembly_code

    def compile_main(self, main):
        var_declarations = main[1]
        for var in var_declarations:
            if var[0] == 'T':
                self.symbols.put(Array(var[0], var[1]), DataType.ARRAY)
            else:
                self.symbols.put(Variable(var), DataType.VARIABLE)
        commands = main[2]
        assembly_code = self.generate_from_commands(commands, 'main')
        return assembly_code
    
    def generate_value(self, num, reg='a'):
        assembly_code = [Code('RST', reg)]
        if num == 0:
            return assembly_code
        if num == 1:
            return assembly_code + [Code('INC', reg)]
        s = str(bin(num))[2:]
        for char in s[:-1]:
            if char == '1':
                assembly_code += [Code('INC', reg)]
            assembly_code += [Code('SHL', reg)]
        if s[len(s) - 1] == '1':
            assembly_code += [Code('INC', reg)]
        return assembly_code

    def generate_from_commands(self, commands, proc_name):
        assembly = []
        for command in commands:
            if command[0] == 'read':
                assembly += self.prepare_identifier_address(command[1], 'b', 'c', True, proc_name)
                assembly += [Code('READ'), Code('STORE', 'b')]
            elif command[0] == 'write':
                assembly += self.prepare_value(command[1], 'a', 'b', proc_name)
                assembly += [Code('WRITE')]
            elif command[0] == 'assign':
                assembly += self.calculate_expression(command[2], proc_name)
                assembly += [Code('PUT', 'h')]
                assembly += self.prepare_identifier_address(command[1], 'b', 'c', True, proc_name)
                assembly += [Code('GET', 'h')]
                assembly += [Code('STORE', 'b')]
            elif command[0] == 'if':
                then_commands = self.generate_from_commands(command[2], proc_name)
                label_false = self.labeler.get_label(off_by_one=True)
                then_commands[-1].labels += [label_false]
                assembly += self.check_condition(command[1], label_false, proc_name)
                assembly += then_commands
            elif command[0] == 'ifelse':
                then_commands = self.generate_from_commands(command[2], proc_name)
                else_commands = self.generate_from_commands(command[3], proc_name)
                label_false = self.labeler.get_label()
                label_endif = self.labeler.get_label(off_by_one=True)
                then_commands += [Code('JUMP', label_endif)]
                else_commands[0].labels += [label_false]
                else_commands[-1].labels += [label_endif]
                assembly += self.check_condition(command[1], label_false, proc_name)
                assembly += then_commands
                assembly += else_commands
            elif command[0] == 'while':
                do_commands = self.generate_from_commands(command[2], proc_name)
                label_false = self.labeler.get_label(off_by_one=True)
                cond_code = self.check_condition(command[1], label_false, proc_name)
                label_loop = self.labeler.get_label()
                cond_code[0].labels += [label_loop]
                do_commands += [Code('JUMP', label_loop)]
                do_commands[-1].labels += [label_false]
                assembly += cond_code
                assembly += do_commands
            elif command[0] == 'repeat':
                do_commands = self.generate_from_commands(command[1], proc_name)
                label_false = self.labeler.get_label()
                do_commands[0].labels += [label_false]
                cond_code = self.check_condition(command[2], label_false, proc_name)
                assembly += do_commands
                assembly += cond_code
            elif command[0] == 'proc_call':
                procedure = self.symbols.get_procedure(command[1], proc_name)
                if len(procedure.args) != len(command[2]): #@TODO zmienic na angielski
                    print(f'BŁĄD: procedura \"{command[1]}\" wymaga {len(procedure.args)} argumentów, a podano {len(command[2])}')
                argv_pointer = procedure.address
                assembly += self.generate_value(argv_pointer, 'a')
                assembly += [Code('PUT', 'b')]
                assembly += [Code('PUT', 'c')]
                for i in range(len(procedure.args)):
                    assembly += [Code('INC', 'b')]
                    is_param = False
                    if type(procedure.args[i]) is tuple:
                        if self.symbols.is_array(command[2][i], proc_name):
                            addr = self.symbols.get_array_address(command[2][i], proc_name)
                        else:
                            addr = self.symbols.get_procedure_parameter_address(command[2][i], proc_name)
                            is_param = True
                    else:
                        if self.symbols.is_variable(command[2][i], proc_name):
                            addr = self.symbols.get_variable_address(command[2][i], True, proc_name)
                        else:
                            addr = self.symbols.get_procedure_parameter_address(command[2][i], proc_name)
                            is_param = True
                    assembly += self.generate_value(addr, 'a')
                    if is_param:
                        assembly += [Code('LOAD', 'a')]
                    assembly += [Code('STORE', 'b')]
                assembly += [
                    Code('RST', 'a'),
                    Code('INC', 'a'),
                    Code('SHL', 'a'),
                    Code('SHL', 'a'),
                    Code('STRK', 'd'),
                    Code('ADD', 'd'),
                    Code('STORE', 'c'),
                    Code('JUMP', f'l_PROCEDURE_{command[1]}')
                ]
        return assembly

    def prepare_value(self, val, target_reg='a', temp_reg='b', proc_name='main'):
        assembly_code = []
        if type(val) is int:
            assembly_code += self.generate_value(val, target_reg)
        else:
            assembly_code += self.prepare_identifier_address(val, target_reg, temp_reg, False, proc_name)
            assembly_code += [Code('LOAD', target_reg)]
            if target_reg != 'a':
                assembly_code += [Code('PUT', target_reg)]
        return assembly_code

    def prepare_identifier_address(self, identifier, target_reg='a', temp_reg='b', write=True, proc_name='main'):
        if proc_name == 'main':
            assembly_code = []
            if type(identifier) is tuple:
                if type(identifier[1]) is int:  # pidentifier[num]
                    adr = self.symbols.get_array_element_adr_const(identifier[0], identifier[1], write, 'main')
                    assembly_code += self.generate_value(adr, target_reg)
                else:  # pidentifier[pidentifier]
                    array_addr = self.symbols.get_array_address(identifier[0], 'main')
                    index_var_addr = self.symbols.get_variable_address(identifier[1], False, 'main')
                    assembly_code += self.generate_value(index_var_addr, temp_reg)
                    assembly_code += [Code('LOAD', temp_reg)]
                    assembly_code += self.generate_value(array_addr, temp_reg)
                    assembly_code += [Code('ADD', temp_reg)]
                    if target_reg != 'a':
                        assembly_code += [Code('PUT', target_reg)]
            else:  # pidentifier
                var_addr = self.symbols.get_variable_address(identifier, write, 'main')
                assembly_code += self.generate_value(var_addr, target_reg)
            return assembly_code
        else:
            assembly_code = []
            if type(identifier) is tuple:
                if type(identifier[1]) is int:  # pidentifier[num]
                    if self.symbols.is_array(identifier[0], proc_name):
                        adr = self.symbols.get_array_element_adr_const(identifier[0], identifier[1], write, proc_name)
                        assembly_code += self.generate_value(adr, target_reg)
                    else:
                        adr = self.symbols.get_procedure_parameter_address(identifier[0], proc_name)
                        assembly_code += self.generate_value(adr, temp_reg)
                        assembly_code += [Code('LOAD', temp_reg)]
                        assembly_code += self.generate_value(identifier[1], temp_reg)
                        assembly_code += [Code('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Code('PUT', target_reg)]
                else:  # pidentifier[pidentifier]
                    if self.symbols.is_array(identifier[0], proc_name) and self.symbols.is_variable(identifier[1], proc_name):
                        # variable[variable]
                        array_addr = self.symbols.get_array_address(identifier[0], proc_name)
                        index_var_addr = self.symbols.get_variable_address(identifier[1], False, proc_name)
                        assembly_code += self.generate_value(index_var_addr, temp_reg)
                        assembly_code += [Code('LOAD', temp_reg)]
                        assembly_code += self.generate_value(array_addr, temp_reg)
                        assembly_code += [Code('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Code('PUT', target_reg)]
                    elif self.symbols.is_array(identifier[0], proc_name) and (not self.symbols.is_variable(identifier[1], proc_name)):
                        # variable[parameter]
                        array_addr = self.symbols.get_array_address(identifier[0], proc_name)
                        index_var_addr = self.symbols.get_procedure_parameter_address(identifier[1], proc_name)
                        assembly_code += self.generate_value(index_var_addr, temp_reg)
                        assembly_code += [Code('LOAD', temp_reg)]
                        assembly_code += [Code('LOAD', 'a')]
                        assembly_code += self.generate_value(array_addr, temp_reg)
                        assembly_code += [Code('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Code('PUT', target_reg)]
                    elif (not self.symbols.is_array(identifier[0], proc_name)) and self.symbols.is_variable(identifier[1], proc_name):
                        # parameter[variable]
                        array_addr = self.symbols.get_procedure_parameter_address(identifier[0], proc_name)
                        index_var_addr = self.symbols.get_variable_address(identifier[1], False, proc_name)
                        assembly_code += self.generate_value(index_var_addr, temp_reg)
                        assembly_code += [Code('LOAD', temp_reg)]
                        assembly_code += [Code('PUT', temp_reg)]
                        assembly_code += self.generate_value(array_addr, target_reg)
                        assembly_code += [Code('LOAD', target_reg)]
                        assembly_code += [Code('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Code('PUT', target_reg)]
                    else:
                        # parameter[parameter]
                        array_addr = self.symbols.get_procedure_parameter_address(identifier[0], proc_name)
                        index_var_addr = self.symbols.get_procedure_parameter_address(identifier[1], proc_name)
                        assembly_code += self.generate_value(index_var_addr, temp_reg)
                        assembly_code += [Code('LOAD', temp_reg)]
                        assembly_code += [Code('LOAD', 'a')]
                        assembly_code += [Code('PUT', temp_reg)]
                        assembly_code += self.generate_value(array_addr, target_reg)
                        assembly_code += [Code('LOAD', target_reg)]
                        assembly_code += [Code('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Code('PUT', target_reg)]
            else:  # pidentifier
                if self.symbols.is_variable(identifier, proc_name):
                    var_addr = self.symbols.get_variable_address(identifier, write, proc_name)
                    assembly_code += self.generate_value(var_addr, target_reg)
                else:
                    var_addr = self.symbols.get_procedure_parameter_address(identifier, proc_name)
                    assembly_code += self.generate_value(var_addr, temp_reg)
                    assembly_code += [Code('LOAD', temp_reg)]
                    if target_reg != 'a':
                        assembly_code += [Code('PUT', target_reg)]
            return assembly_code
        
    def check_condition(self, cond, label_false, proc_name='main'):
        assembly_code = []
        operator = cond[0]
        num1 = cond[1]
        num2 = cond[2]
        if operator == '=' or operator == '!=':
            assembly_code += self.prepare_value(num1, target_reg='c', temp_reg='b', proc_name=proc_name)
            assembly_code += self.prepare_value(num2, target_reg='d', temp_reg='b', proc_name=proc_name)
            assembly_code += [(Code('GET', 'd'))]
            assembly_code += [(Code('SUB', 'c'))]
            assembly_code += [(Code('PUT', 'e'))]
            assembly_code += [(Code('GET', 'c'))]
            assembly_code += [(Code('SUB', 'd'))]
            assembly_code += [(Code('ADD', 'e'))]
            if operator == '=':
                assembly_code += [(Code('JPOS', label_false))]
            else:
                assembly_code += [(Code('JZERO', label_false))]
        elif operator == '>':
            assembly_code += self.prepare_value(num1, target_reg='c', temp_reg='b', proc_name=proc_name)
            assembly_code += self.prepare_value(num2, target_reg='d', temp_reg='b', proc_name=proc_name)
            assembly_code += [Code('GET', 'c')]
            assembly_code += [Code('SUB', 'd')]
            assembly_code += [Code('JZERO', label_false)]
        elif operator == '<':
            assembly_code += self.prepare_value(num1, target_reg='c', temp_reg='b', proc_name=proc_name)
            assembly_code += self.prepare_value(num2, target_reg='d', temp_reg='b', proc_name=proc_name)
            assembly_code += [Code('GET', 'd')]
            assembly_code += [Code('SUB', 'c')]
            assembly_code += [Code('JZERO', label_false)]
        elif operator == '>=':
            assembly_code += self.prepare_value(num1, target_reg='c', temp_reg='b', proc_name=proc_name)
            assembly_code += self.prepare_value(num2, target_reg='d', temp_reg='b', proc_name=proc_name)
            assembly_code += [Code('GET', 'd')]
            assembly_code += [Code('SUB', 'c')]
            assembly_code += [Code('JPOS', label_false)]
        elif operator == '<=':
            assembly_code += self.prepare_value(num1, target_reg='c', temp_reg='b', proc_name=proc_name)
            assembly_code += self.prepare_value(num2, target_reg='d', temp_reg='b', proc_name=proc_name)
            assembly_code += [Code('GET', 'c')]
            assembly_code += [Code('SUB', 'd')]
            assembly_code += [Code('JPOS', label_false)]
        return assembly_code
            
    def calculate_expression(self, expr, proc_name='main'):
        assembly_code = []
        operator = expr[0]
        num1 = expr[1]
        if operator == 'val':
            assembly_code += self.prepare_value(num1, target_reg='a', temp_reg='b', proc_name=proc_name)
        else:
            num2 = expr[2]
        if operator == '+' or operator == '-':
            assembly_code += self.prepare_value(num1, target_reg='c', temp_reg='b', proc_name=proc_name)
            assembly_code += self.prepare_value(num2, target_reg='d', temp_reg='b', proc_name=proc_name)
            assembly_code += [Code('GET', 'c')]
            if operator == '+':
                assembly_code += [Code('ADD', 'd')]
            else:
                assembly_code += [Code('SUB', 'd')]
        elif operator == '*':
            label_skip = self.labeler.get_label(off_by_one=True)
            assembly_code += self.prepare_value(num2, target_reg='a', temp_reg='c', proc_name=proc_name)
            assembly_code += [Code('JZERO', label_skip),
                      Code('PUT', 'b')]
            assembly_code += self.prepare_value(num1, target_reg='a', temp_reg='c', proc_name=proc_name)
            assembly_code += [Code('JZERO', label_skip),
                      Code('PUT', 'c')]
            label_loop = self.labeler.get_label()
            label_even = self.labeler.get_label()
            assembly_code += [
                Code('RST', 'd'),
                Code('SHR', 'c', [label_loop]),
                Code('SHL', 'c'),
                Code('SUB', 'c'),
                Code('JZERO', label_even),
                Code('GET', 'd'),
                Code('ADD', 'b'),
                Code('PUT', 'd'),
                Code('SHL', 'b', [label_even]),
                Code('SHR', 'c'),
                Code('GET', 'c'),
                Code('JPOS', label_loop),
                Code('GET', 'd', [label_skip]),
            ]
        elif operator == '/' or operator == '%':
            label_skip = self.labeler.get_label(off_by_one=True)
            assembly_code += self.prepare_value(num2, target_reg='a', temp_reg='c', proc_name=proc_name)
            assembly_code += [Code('JZERO', label_skip),
                      Code('PUT', 'b')]
            assembly_code += self.prepare_value(num1, target_reg='a', temp_reg='c', proc_name=proc_name)
            assembly_code += [Code('JZERO', label_skip)]

            label_begin = self.labeler.get_label()
            label_loop = self.labeler.get_label()
            label_end = self.labeler.get_label()
            label_shl_enter = self.labeler.get_label()
            label_shl_exit = self.labeler.get_label()
            assembly_code += [
                Code('RST', 'e'),
                Code('JUMP', label_begin),
                Code('SUB', 'c', [label_loop]),
                Code('PUT', 'f', [label_begin]),
                Code('GET', 'b'),
                Code('SUB', 'f'),
                Code('JPOS', label_end),
                Code('GET', 'b'),
                Code('PUT', 'c'),
                Code('RST', 'd'),
                Code('INC', 'd'),
                Code('GET', 'f', [label_shl_exit]),
                Code('SHL', 'c'),
                Code('SUB', 'c'),
                Code('JPOS', label_shl_enter),
                Code('SHR', 'c'),
                Code('GET', 'e'),
                Code('ADD', 'd'),
                Code('PUT', 'e'),
                Code('GET', 'f'),
                Code('JUMP', label_loop),
                Code('SHL', 'd', [label_shl_enter]),
                Code('JUMP', label_shl_exit),
            ]
            if operator == '/':
                assembly_code += [Code('GET', 'e', [label_end, label_skip])]
            else:
                assembly_code += [Code('GET', 'f', [label_end, label_skip])]

        return assembly_code