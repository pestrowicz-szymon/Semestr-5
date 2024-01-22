from my_symbol_table import SymbolTable
from my_code import Code
from my_array import Array
from my_variable import Variable
from my_labeler import Labeler

class CodeGenerator:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def generate_executable(self, parser_result):
        proc_code = []
        for procedure in parser_result[1]:
            proc_code += self.generate_procedure(procedure)

        codes = self.generate_main(parser_result[2])
        codes += [Code('HALT')]
        codes += proc_code
        return codes

    def generate_main(self, parser_result):
        declarations = parser_result[1]
        for declaration in declarations:
            if isinstance(declaration, tuple):
                self.symbol_table.put_array(Array(declaration[0], declaration[1]))
            else:
                self.symbol_table.put_variable(Variable(declaration))
        commands = parser_result[2]
        codes = self.generate_from_commands(commands, 'main')
        return codes
    
    def generate_from_commands(self, commands, proc_name):
        codes = []
        for command in commands:
            if command[0] == 'read':
                codes += [Code('READ')]
                codes += [Code('RST', 'b')]
                for i in range(self.symbol_table.get_variable_address(command[1], True)):
                    codes += [Code('INC', 'b')]
                codes += [Code('STORE', 'b')]
            if command[0] == 'write':
                if command[1].isdigit():
                    codes += [Code('RST', 'a')]
                    for i in range(int(command[1])):
                        codes += [Code('INC', 'a')]
                    codes += [Code('WRITE')]
                else:
                    codes += [Code('RST', 'b')]
                    for i in range(self.symbol_table.get_variable_address(command[1], False)):
                        codes += [Code('INC', 'b')]
                    codes += [Code('LOAD', 'b')]
                    codes += [Code('WRITE')]
            if command[0] == 'assign':
                codes += self.calculate_expression(command[2])
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

        return codes
    
    def get_value(self, value, target_register='a', temporary_register='b', proc_name='main'):
        codes = []
        if value.isdigit():
            codes += self.generate_constant_value(value, target_register)           
        else:
            codes += self.prepare_identifier_address(value, target_register, temporary_register, False, proc_name)
            codes += [Code('LOAD', target_register)]
            if target_register != 'a':
                codes += [Code('PUT', target_register)]
        return codes
    
    def generate_constant_value(self, value, register='a'):
        codes = [Code('RST', register)]
        for i in range(value):
            codes += [Code('INC', register)]
        return codes
    
    def create_condition(self, condition, label_true, label_false, proc_name='main'):
        codes = []
        operator = condition[1]
        if operator == '=':
            self.get_value(condition[0], 'c', 'b', proc_name)
            self.get_value(condition[1], 'd', 'b', proc_name)


            self.code.append(f'GET b')
            self.code.append(f'SUB c')
            self.code.append(f'PUT d')
            self.code.append(f'GET c')
            self.code.append(f'SUB b')
            self.code.append(f'ADD d')
            self.IF_JUMPS_POSITIONS.append(len(self.code))
            self.code.append(f'JPOS to_change')
        if operator == '!=':
            self.get_value(num1, 'b')
            self.get_value(num2, 'c')
            self.code.append(f'GET b')
            self.code.append(f'SUB c')
            self.code.append(f'PUT d')
            self.code.append(f'GET c')
            self.code.append(f'SUB b')
            self.code.append(f'ADD d')
            self.IF_JUMPS_POSITIONS.append(len(self.code))
            self.code.append(f'JZERO to_change')
        if operator == '>':
            self.get_value(num1, 'b')
            self.get_value(num2, 'c')
            self.code.append('GET b')
            self.code.append('SUB c')
            self.IF_JUMPS_POSITIONS.append(len(self.code))
            self.code.append(f'JZERO to_change')
            
        if operator == '<':
            pass
        if operator == '>=':
            pass
        if operator == '<=':
            pass
    
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

    
























    def gen_code_from_commands(self, main):
        #for procedure in procedures:
        #    self.code.append(procedure)
        for code in main:
            print(code)

            # ---------- READ -------------------------------------
            if code[0] == 'read':
                self.code.append(f'READ')
                self.code.append(f'RST b')
                for i in range(self.symbols.get_address(code[1])):
                    self.code.append(f'INC b')
                self.code.append(f'STORE b')


            # ---------- WRITE -------------------------------------
            if code[0] == 'write':
                if code[1].isdigit:
                    self.code.append(f'RST a')
                    for i in range(int(code[1])):
                        self.code.append(f'INC a')
                    self.code.append(f'WRITE')
                else:
                    self.code.append(f'RST b')
                    for i in range(self.symbols.get_address(code[1])):
                        self.code.append(f'INC b')
                    self.code.append(f'LOAD b')
                    self.code.append(f'WRITE')


            # ---------- ASSIGN -------------------------------------
            if code[0] == 'assign':     
                    self.code.append(f'RST b')                          
                    for i in range(self.symbols.get_address(code[1])):
                        self.code.append(f'INC b')                       
                    self.create_expression(code[2], 'a')                       
                    self.code.append(f'STORE b')   


            # ---------- IF ------------------------------------- 
            if code[0] == 'if': 
                self.create_condition(code[1])
                self.gen_code_from_commands(code[2])
                AFTER_COMMANDS_POSITION = len(self.code)
                JUMP_POSITION = self.IF_JUMPS_POSITIONS.pop()
                self.code[JUMP_POSITION] = self.code[JUMP_POSITION].replace('to_change', str(AFTER_COMMANDS_POSITION))

            # ---------- IF ELSE -------------------------------------
            if code[0] == 'ifelse':
                self.create_condition(code[1])
                self.gen_code_from_commands(code[2])
                ELSE_POSITION = len(self.code)+1
                JUMP_POSITION = self.IF_JUMPS_POSITIONS.pop()
                self.code[JUMP_POSITION] = self.code[JUMP_POSITION].replace('to_change', str(ELSE_POSITION))
                self.IF_JUMPS_POSITIONS.append(len(self.code))

                self.code.append(f'JUMP to_change')
                self.gen_code_from_commands(code[3])
                ELSE_POSITION = len(self.code)
                JUMP_POSITION = self.IF_JUMPS_POSITIONS.pop()
                self.code[JUMP_POSITION] = self.code[JUMP_POSITION].replace('to_change', str(ELSE_POSITION))

            # ---------- WHILE -------------------------------------
            if code[0] == 'while':
                CONDITION_POSITION = len(self.code)
                self.create_condition(code[1])
                self.gen_code_from_commands(code[2])
                OUT_WHILE_POSITION = len(self.code)+1
                JUMP_POSITION = self.IF_JUMPS_POSITIONS.pop()
                self.code[JUMP_POSITION] = self.code[JUMP_POSITION].replace('to_change', str(OUT_WHILE_POSITION))
                self.code.append(f'JUMP {CONDITION_POSITION}')

            # ---------- REPEAT -------------------------------------
            if code[0] == 'repeat':
                BEFORE_COMMANDS_POSITION = len(self.code)
                self.gen_code_from_commands(code[1])
                self.create_condition(code[2])
                JUMP_POSITION = self.IF_JUMPS_POSITIONS.pop()
                self.code[JUMP_POSITION] = f'JPOS {BEFORE_COMMANDS_POSITION}'





                

    def create_condition(self, code):
        num1 = code[0]
        num2 = code[2]
        operator = code[1]
        if operator == '=':
            self.get_value(num1, 'b')
            self.get_value(num2, 'c')
            self.code.append(f'GET b')
            self.code.append(f'SUB c')
            self.code.append(f'PUT d')
            self.code.append(f'GET c')
            self.code.append(f'SUB b')
            self.code.append(f'ADD d')
            self.IF_JUMPS_POSITIONS.append(len(self.code))
            self.code.append(f'JPOS to_change')
        if operator == '!=':
            self.get_value(num1, 'b')
            self.get_value(num2, 'c')
            self.code.append(f'GET b')
            self.code.append(f'SUB c')
            self.code.append(f'PUT d')
            self.code.append(f'GET c')
            self.code.append(f'SUB b')
            self.code.append(f'ADD d')
            self.IF_JUMPS_POSITIONS.append(len(self.code))
            self.code.append(f'JZERO to_change')
        if operator == '>':
            self.get_value(num1, 'b')
            self.get_value(num2, 'c')
            self.code.append('GET b')
            self.code.append('SUB c')
            self.IF_JUMPS_POSITIONS.append(len(self.code))
            self.code.append(f'JZERO to_change')
            
        if operator == '<':
            pass
        if operator == '>=':
            pass
        if operator == '<=':
            pass

    def get_value(self, value, register):
        self.code.append(f'RST {register}')
        if value.isdigit():
            for i in range(int(value)):
                self.code.append(f'INC {register}')              
        else:
            for i in range(self.symbols.get_address(value)):
                self.code.append(f'INC {register}')
            self.code.append(f'LOAD {register}')
            self.code.append(f'PUT {register}')


    # code - tuple from parser or number
    # register - at which register save result
    def create_expression(self, code, register):
        self.code.append(f'RST {register}') 
        if isinstance(code, str):                        
            if code.isdigit():
                for i in range(int(code)):
                    self.code.append(f'INC {register}')              
            else:
                for i in range(self.symbols.get_address(code)):
                    self.code.append(f'INC {register}')
                self.code.append(f'LOAD {register}')
        else:             
            if code[1].isdigit() & code[2].isdigit():
                for i in range(self.calculate_expression(code[0], code[1], code[2])):
                    self.code.append(f'INC {register}')
            else:
                self.get_value(code[1], 'c')
                self.get_value(code[2], 'd')
                if code[0] == '+':
                    self.code.append(f'GET c')
                    self.code.append(f'ADD d')
                    self.code.append(f'PUT e')
                elif code[0] == '-':
                    self.code.append(f'GET c')
                    self.code.append(f'SUB d')
                    self.code.append(f'PUT e')
                elif code[0] == '*':
                    self.code.append(f'RST e')
                    LABEL_LOOP = len(self.code)
                    self.code.append(f'SHR c')
                    self.code.append(f'SHL c')
                    self.code.append(f'SUB c')
                    JZERO = len(self.code)
                    self.code.append(f'JZERO to_change')
                    self.code.append(f'GET e')
                    self.code.append(f'ADD d')
                    self.code.append(f'PUT e')
                    LABEL_EVEN = len(self.code)
                    self.code[JZERO] = self.code[JZERO].replace('to_change', str(LABEL_EVEN))
                    self.code.append(f'SHL d')
                    self.code.append(f'SHR c')
                    self.code.append(f'GET c')
                    self.code.append(f'JPOS {LABEL_LOOP}')
                    self.code.append(f'GET e')
                elif code[0] == '/' or code[0] == '%':
                    self.code.append(f'RST e')
                    BEGIN_JUMP = len(self.code)
                    self.code.append(f'JUMP to_change')
                    LABEL_LOOP = len(self.code)
                    self.code.append(f'SUB f')
                    LABEL_BEGIN = len(self.code)
                    self.code[BEGIN_JUMP] = self.code[BEGIN_JUMP].replace('to_change', str(LABEL_BEGIN))
                    self.code.append(f'PUT c')
                    self.code.append(f'GET d')
                    self.code.append(f'SUB c')
                    END_JUMP = len(self.code)
                    self.code.append(f'JPOS to_change')
                    self.code.append(f'GET d')
                    self.code.append(f'PUT f')
                    self.code.append(f'RST h')
                    self.code.append(f'INC h')
                    SHL_EXIT = len(self.code)
                    self.code.append(f'GET c')
                    self.code.append(f'SHL f')
                    self.code.append(f'SUB f')
                    JUMP_SHL_ENTER = len(self.code)
                    self.code.append(f'JPOS to_change')
                    self.code.append(f'SHR f')
                    self.code.append(f'GET e')
                    self.code.append(f'ADD h')
                    self.code.append(f'PUT e')
                    self.code.append(f'GET c')
                    self.code.append(f'JUMP {LABEL_LOOP}')
                    SHL_ENTER = len(self.code)
                    self.code.append(f'SHL h')
                    self.code[JUMP_SHL_ENTER] = self.code[JUMP_SHL_ENTER].replace('to_change', str(SHL_ENTER))
                    self.code.append(f'JUMP {SHL_EXIT}')

                    LABEL_END = len(self.code)
                    self.code[END_JUMP] = self.code[END_JUMP].replace('to_change', str(LABEL_END))
                    if code[0] == '/':
                        self.code.append(f'GET e')
                    else:
                        self.code.append(f'GET c')




                    


                
    # return expression result
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
        