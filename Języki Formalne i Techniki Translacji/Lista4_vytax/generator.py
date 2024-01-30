from my_array import Array
from my_pair import Pair
from my_labeler import Labeler
from my_procedure_data import ProcedureData
from my_symbol_table import SymbolTable, DataType
from my_variable import Variable

#@TODO change labels

class Generator:
    def __init__(self):
        self.symbols = SymbolTable()
        self.labeler = Labeler()

    def compile_all(self, parser_result):
        procedures_result = []
        for procedure in parser_result[1]:
            procedures_result += self.compile_procedure(procedure)

        main_result = self.compile_main(parser_result[2])
        main_result[0].labels += ['l_main']

        assembly_code = [Pair('JUMP', 'l_main')]
        assembly_code += procedures_result
        assembly_code += main_result
        assembly_code += [Pair('HALT')]

        #remove labels from jump function
        l_dictionary = dict()
        for i in range(len(assembly_code)):
            for label in assembly_code[i].l_dictionary:
                if label[1] == '-':
                    l_dictionary[label] = i + 1
                else:
                    l_dictionary[label] = i
        for code in assembly_code:
            code.l_dictionary = []
            if code.arg is not None and str(code.arg)[0] == 'l':
                code.arg = l_dictionary[code.arg]

        return assembly_code

    def compile_procedure(self, procedure):
        procedure_head = procedure[1]
        procedure_name = procedure_head[1]
        self.symbols.put(ProcedureData(procedure_name, procedure_head[2]), DataType.PROCEDURE)
        declarations = procedure[2]
        for declaration in declarations:
            if type(declaration) is tuple:
                self.symbols.put(Array(declaration[0], declaration[1]), DataType.ARRAY, procedure_name)
            else:
                self.symbols.put(Variable(declaration), DataType.VARIABLE,procedure_name)
        lines = procedure[3]
        assembly_code = self.make_all(lines, procedure_name)
        assembly_code[0].labels += [f'l_PROCEDURE_{procedure_name}']
        return_addr = self.symbols.get_procedure_parameter_address('RET', procedure_name)
        assembly_code += self.generate_value(return_addr, 'a')
        assembly_code += [Pair('LOAD', 'a')]
        assembly_code += [Pair('JUMPR', 'a')]
        return assembly_code

    def compile_main(self, main):
        var_declarations = main[1]
        lines = main[2]
        for var in var_declarations:
            if type(var) is tuple:
                self.symbols.put(Array(var[0], var[1]), DataType.ARRAY)
            else:
                self.symbols.put(Variable(var), DataType.VARIABLE)
        assembly_code = self.make_all(lines, 'main')
        return assembly_code

    def make_all(self, lines, current_procedure_name):
        assembly = []
        for line in lines:
            if line[0] == 'read':
                assembly += self.get_id_at_address(line[1], 'b', 'c', True, current_procedure_name)
                assembly += [Pair('READ'), Pair('STORE', 'b')]
            elif line[0] == 'write':
                assembly += self.get_value(line[1], 'a', 'b', current_procedure_name)
                assembly += [Pair('WRITE')]
            elif line[0] == 'assign':
                assembly += self.get_operation_value(line[2], current_procedure_name)
                assembly += [Pair('PUT', 'g')]
                assembly += self.get_id_at_address(line[1], 'b', 'c', True, current_procedure_name)
                assembly += [Pair('GET', 'g')]
                assembly += [Pair('STORE', 'b')]
            elif line[0] == 'if':
                then_code = self.make_all(line[2], current_procedure_name)
                l_false = self.labeler.get_label(off_by_one=True)
                then_code[-1].labels += [l_false]
                assembly += self.check_condition(line[1], l_false, current_procedure_name)
                assembly += then_code
            elif line[0] == 'ifelse':
                then_code = self.make_all(line[2], current_procedure_name)
                else_code = self.make_all(line[3], current_procedure_name)
                l_false = self.labeler.get_label()
                l_endif = self.labeler.get_label(off_by_one=True)
                then_code += [Pair('JUMP', l_endif)]
                else_code[0].labels += [l_false]
                else_code[-1].labels += [l_endif]
                assembly += self.check_condition(line[1], l_false, current_procedure_name)
                assembly += then_code
                assembly += else_code
            elif line[0] == 'while':
                do_lines = self.make_all(line[2], current_procedure_name)
                l_false = self.labeler.get_label(off_by_one=True)
                cond_code = self.check_condition(line[1], l_false, current_procedure_name)
                l_loop = self.labeler.get_label()
                cond_code[0].labels += [l_loop]
                do_lines += [Pair('JUMP', l_loop)]
                do_lines[-1].labels += [l_false]
                assembly += cond_code
                assembly += do_lines
            elif line[0] == 'repeat':
                do_lines = self.make_all(line[1], current_procedure_name)
                l_false = self.labeler.get_label()
                do_lines[0].labels += [l_false]
                cond_code = self.check_condition(line[2], l_false, current_procedure_name)
                assembly += do_lines
                assembly += cond_code
            elif line[0] == 'proc_call':
                procedure = self.symbols.get_procedure(line[1], current_procedure_name)
                if len(procedure.args) != len(line[2]):
                    print(f'Error: \"{line[1]}\" needs {len(procedure.args)} values')
                argv_pointer = procedure.address
                assembly += self.generate_value(argv_pointer, 'a')
                assembly += [Pair('PUT', 'b')]
                assembly += [Pair('PUT', 'c')]
                for i in range(len(procedure.args)):
                    assembly += [Pair('INC', 'b')]
                    is_param = False
                    if type(procedure.args[i]) is tuple:
                        if self.symbols.is_array(line[2][i], current_procedure_name):
                            addr = self.symbols.get_array_address(line[2][i], current_procedure_name)
                        else:
                            addr = self.symbols.get_procedure_parameter_address(line[2][i], current_procedure_name)
                            is_param = True
                    else:
                        if self.symbols.is_variable(line[2][i], current_procedure_name):
                            addr = self.symbols.get_variable_address(line[2][i], True, current_procedure_name)
                        else:
                            addr = self.symbols.get_procedure_parameter_address(line[2][i], current_procedure_name)
                            is_param = True
                    assembly += self.generate_value(addr, 'a')
                    if is_param:
                        assembly += [Pair('LOAD', 'a')]
                    assembly += [Pair('STORE', 'b')]
                assembly += [
                    Pair('RST', 'a'),
                    Pair('INC', 'a'),
                    Pair('SHL', 'a'),
                    Pair('SHL', 'a'),
                    Pair('STRK', 'd'),
                    Pair('ADD', 'd'),
                    Pair('STORE', 'c'),
                    Pair('JUMP', f'l_PROCEDURE_{line[1]}')
                ]
        return assembly

    def get_value(self, val, target_reg='a', temp_reg='h', proc_name='main'):
        assembly_code = []
        if type(val) is int:
            assembly_code += self.generate_value(val, target_reg)
        else:
            assembly_code += self.get_id_at_address(val, target_reg, temp_reg, False, proc_name)
            assembly_code += [Pair('LOAD', target_reg)]
            assembly_code += [Pair('PUT', target_reg)]
        return assembly_code
    
    def generate_value(self, num, reg='a'):
        assembly_code = [Pair('RST', reg)]
        if num == 0:
            return assembly_code
        if num == 1:
            return assembly_code + [Pair('INC', reg)]
        s = str(bin(num))[2:]
        for char in s[:-1]:
            if char == '1':
                assembly_code += [Pair('INC', reg)]
            assembly_code += [Pair('SHL', reg)]
        if s[len(s) - 1] == '1':
            assembly_code += [Pair('INC', reg)]
        return assembly_code

    def get_id_at_address(self, identifier, target_reg='a', temp_reg='h', is_initialized=True, procedure_name='main'):
        if procedure_name == 'main':
            assembly_code = []
            if type(identifier) is tuple:
                if type(identifier[1]) is int:
                    address = self.symbols.get_array_element_adr_const(identifier[0], identifier[1], is_initialized, 'main')
                    assembly_code += self.generate_value(address, target_reg)
                else:
                    array_addr = self.symbols.get_array_address(identifier[0], 'main')
                    index_var_addr = self.symbols.get_variable_address(identifier[1], False, 'main')
                    assembly_code += self.generate_value(index_var_addr, temp_reg)
                    assembly_code += [Pair('LOAD', temp_reg)]
                    assembly_code += self.generate_value(array_addr, temp_reg)
                    assembly_code += [Pair('ADD', temp_reg)]
                    if target_reg != 'a':
                        assembly_code += [Pair('PUT', target_reg)]
            else:
                var_addr = self.symbols.get_variable_address(identifier, is_initialized, 'main')
                assembly_code += self.generate_value(var_addr, target_reg)
            return assembly_code
        else:
            assembly_code = []
            if type(identifier) is tuple:
                if type(identifier[1]) is int:
                    if self.symbols.is_array(identifier[0], procedure_name):
                        address = self.symbols.get_array_element_adr_const(identifier[0], identifier[1], is_initialized, procedure_name)
                        assembly_code += self.generate_value(address, target_reg)
                    else:
                        address = self.symbols.get_procedure_parameter_address(identifier[0], procedure_name)
                        assembly_code += self.generate_value(address, temp_reg)
                        assembly_code += [Pair('LOAD', temp_reg)]
                        assembly_code += self.generate_value(identifier[1], temp_reg)
                        assembly_code += [Pair('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Pair('PUT', target_reg)]
                else:
                    if self.symbols.is_array(identifier[0], procedure_name) and self.symbols.is_variable(identifier[1], procedure_name):
                        array_addr = self.symbols.get_array_address(identifier[0], procedure_name)
                        index_var_addr = self.symbols.get_variable_address(identifier[1], False, procedure_name)
                        assembly_code += self.generate_value(index_var_addr, temp_reg)
                        assembly_code += [Pair('LOAD', temp_reg)]
                        assembly_code += self.generate_value(array_addr, temp_reg)
                        assembly_code += [Pair('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Pair('PUT', target_reg)]
                    elif self.symbols.is_array(identifier[0], procedure_name) and (not self.symbols.is_variable(identifier[1], procedure_name)):
                        array_addr = self.symbols.get_array_address(identifier[0], procedure_name)
                        index_var_addr = self.symbols.get_procedure_parameter_address(identifier[1], procedure_name)
                        assembly_code += self.generate_value(index_var_addr, temp_reg)
                        assembly_code += [Pair('LOAD', temp_reg)]
                        assembly_code += [Pair('LOAD', 'a')]
                        assembly_code += self.generate_value(array_addr, temp_reg)
                        assembly_code += [Pair('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Pair('PUT', target_reg)]
                    elif (not self.symbols.is_array(identifier[0], procedure_name)) and self.symbols.is_variable(identifier[1], procedure_name):
                        array_addr = self.symbols.get_procedure_parameter_address(identifier[0], procedure_name)
                        index_var_addr = self.symbols.get_variable_address(identifier[1], False, procedure_name)
                        assembly_code += self.generate_value(index_var_addr, temp_reg)
                        assembly_code += [Pair('LOAD', temp_reg)]
                        assembly_code += [Pair('PUT', temp_reg)]
                        assembly_code += self.generate_value(array_addr, target_reg)
                        assembly_code += [Pair('LOAD', target_reg)]
                        assembly_code += [Pair('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Pair('PUT', target_reg)]
                    else:
                        array_addr = self.symbols.get_procedure_parameter_address(identifier[0], procedure_name)
                        index_var_addr = self.symbols.get_procedure_parameter_address(identifier[1], procedure_name)
                        assembly_code += self.generate_value(index_var_addr, temp_reg)
                        assembly_code += [Pair('LOAD', temp_reg)]
                        assembly_code += [Pair('LOAD', 'a')]
                        assembly_code += [Pair('PUT', temp_reg)]
                        assembly_code += self.generate_value(array_addr, target_reg)
                        assembly_code += [Pair('LOAD', target_reg)]
                        assembly_code += [Pair('ADD', temp_reg)]
                        if target_reg != 'a':
                            assembly_code += [Pair('PUT', target_reg)]
            else:
                if self.symbols.is_variable(identifier, procedure_name):
                    var_addr = self.symbols.get_variable_address(identifier, is_initialized, procedure_name)
                    assembly_code += self.generate_value(var_addr, target_reg)
                else:
                    var_addr = self.symbols.get_procedure_parameter_address(identifier, procedure_name)
                    assembly_code += self.generate_value(var_addr, temp_reg)
                    assembly_code += [Pair('LOAD', temp_reg)]
                    if target_reg != 'a':
                        assembly_code += [Pair('PUT', target_reg)]
            return assembly_code
        
    def check_condition(self, cond, l_false, procedure_name='main'):
        assembly_code = []
        operator = cond[0]
        num1 = cond[1]
        num2 = cond[2]
        if operator == '=' or operator == '!=':
            assembly_code += self.get_value(num1, target_reg='c', temp_reg='h', proc_name=procedure_name)
            assembly_code += self.get_value(num2, target_reg='d', temp_reg='h', proc_name=procedure_name)
            assembly_code += [(Pair('GET', 'd'))]
            assembly_code += [(Pair('SUB', 'c'))]
            assembly_code += [(Pair('PUT', 'e'))]
            assembly_code += [(Pair('GET', 'c'))]
            assembly_code += [(Pair('SUB', 'd'))]
            assembly_code += [(Pair('ADD', 'e'))]
            if operator == '=':
                assembly_code += [(Pair('JPOS', l_false))]
            else:
                assembly_code += [(Pair('JZERO', l_false))]
        elif operator == '>':
            assembly_code += self.get_value(num1, target_reg='c', temp_reg='h', proc_name=procedure_name)
            assembly_code += self.get_value(num2, target_reg='d', temp_reg='h', proc_name=procedure_name)
            assembly_code += [Pair('GET', 'c')]
            assembly_code += [Pair('SUB', 'd')]
            assembly_code += [Pair('JZERO', l_false)]
        elif operator == '<':
            assembly_code += self.get_value(num1, target_reg='c', temp_reg='h', proc_name=procedure_name)
            assembly_code += self.get_value(num2, target_reg='d', temp_reg='h', proc_name=procedure_name)
            assembly_code += [Pair('GET', 'd')]
            assembly_code += [Pair('SUB', 'c')]
            assembly_code += [Pair('JZERO', l_false)]
        elif operator == '>=':
            assembly_code += self.get_value(num1, target_reg='c', temp_reg='h', proc_name=procedure_name)
            assembly_code += self.get_value(num2, target_reg='d', temp_reg='h', proc_name=procedure_name)
            assembly_code += [Pair('GET', 'd')]
            assembly_code += [Pair('SUB', 'c')]
            assembly_code += [Pair('JPOS', l_false)]
        elif operator == '<=':
            assembly_code += self.get_value(num1, target_reg='c', temp_reg='h', proc_name=procedure_name)
            assembly_code += self.get_value(num2, target_reg='d', temp_reg='h', proc_name=procedure_name)
            assembly_code += [Pair('GET', 'c')]
            assembly_code += [Pair('SUB', 'd')]
            assembly_code += [Pair('JPOS', l_false)]
        return assembly_code
            
    def get_operation_value(self, expr, proc_name='main'):
        assembly_code = []
        operator = expr[0]
        num1 = expr[1]
        if operator == 'val':
            assembly_code += self.get_value(num1, target_reg='a', temp_reg='h', proc_name=proc_name)
        else:
            num2 = expr[2]
        if operator == '+' or operator == '-':
            assembly_code += self.get_value(num1, target_reg='c', temp_reg='h', proc_name=proc_name)
            assembly_code += self.get_value(num2, target_reg='d', temp_reg='h', proc_name=proc_name)
            assembly_code += [Pair('GET', 'c')]
            if operator == '+':
                assembly_code += [Pair('ADD', 'd')]
            else:
                assembly_code += [Pair('SUB', 'd')]
        elif operator == '*':
            l_skip = self.labeler.get_label(off_by_one=True)
            assembly_code += self.get_value(num2, target_reg='a', temp_reg='c', proc_name=proc_name)
            assembly_code += [Pair('JZERO', l_skip),
                      Pair('PUT', 'b')]
            assembly_code += self.get_value(num1, target_reg='a', temp_reg='c', proc_name=proc_name)
            assembly_code += [Pair('JZERO', l_skip),
                      Pair('PUT', 'c')]
            l_loop = self.labeler.get_label()
            l_even = self.labeler.get_label()
            assembly_code += [
                Pair('RST', 'd'),
                Pair('SHR', 'c', [l_loop]),
                Pair('SHL', 'c'),
                Pair('SUB', 'c'),
                Pair('JZERO', l_even),
                Pair('GET', 'd'),
                Pair('ADD', 'b'),
                Pair('PUT', 'd'),
                Pair('SHL', 'b', [l_even]),
                Pair('SHR', 'c'),
                Pair('GET', 'c'),
                Pair('JPOS', l_loop),
                Pair('GET', 'd', [l_skip]),
            ]
        elif operator == '/' or operator == '%':
            l_skip = self.labeler.get_label(off_by_one=True)
            assembly_code += self.get_value(num2, target_reg='a', temp_reg='c', proc_name=proc_name)
            assembly_code += [Pair('JZERO', l_skip),
                      Pair('PUT', 'b')]
            assembly_code += self.get_value(num1, target_reg='a', temp_reg='c', proc_name=proc_name)
            assembly_code += [Pair('JZERO', l_skip)]

            l_begin = self.labeler.get_label()
            l_loop = self.labeler.get_label()
            l_end = self.labeler.get_label()
            l_shl_enter = self.labeler.get_label()
            l_shl_exit = self.labeler.get_label()
            assembly_code += [
                Pair('RST', 'e'),
                Pair('JUMP', l_begin),
                Pair('SUB', 'c', [l_loop]),
                Pair('PUT', 'f', [l_begin]),
                Pair('GET', 'b'),
                Pair('SUB', 'f'),
                Pair('JPOS', l_end),
                Pair('GET', 'b'),
                Pair('PUT', 'c'),
                Pair('RST', 'd'),
                Pair('INC', 'd'),
                Pair('GET', 'f', [l_shl_exit]),
                Pair('SHL', 'c'),
                Pair('SUB', 'c'),
                Pair('JPOS', l_shl_enter),
                Pair('SHR', 'c'),
                Pair('GET', 'e'),
                Pair('ADD', 'd'),
                Pair('PUT', 'e'),
                Pair('GET', 'f'),
                Pair('JUMP', l_loop),
                Pair('SHL', 'd', [l_shl_enter]),
                Pair('JUMP', l_shl_exit),
            ]
            if operator == '/':
                assembly_code += [Pair('GET', 'e', [l_end, l_skip])]
            else:
                assembly_code += [Pair('GET', 'f', [l_end, l_skip])]

        return assembly_code