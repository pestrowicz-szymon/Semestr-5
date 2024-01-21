from symbol_table import Variable


class CodeGenerator:
    def __init__(self, procedures, main, symbols):
        self.procedures = procedures
        self.main = main
        self.symbols = symbols
        self.code = []
        self.iterators = []
        self.IF_JUMPS_POSITIONS = []

    def gen_code(self):
        self.gen_code_from_commands(self.main)
        self.code.append("HALT")

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
                if isinstance(code[1], str):
                    self.code.append(f'RST b')
                    for i in range(self.symbols.get_address(code[1])):
                        self.code.append(f'INC b')
                    self.code.append(f'LOAD b')
                    self.code.append(f'WRITE')
                else:
                    self.code.append(f'RST a')
                    for i in range(code[1]):
                        self.code.append(f'INC a')
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
            pass
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
                    self.code.append(f'PUT {register}')
                elif code[0] == '-':
                    self.code.append(f'GET c')
                    self.code.append(f'SUB d')
                    self.code.append(f'PUT {register}')

                
    # return expression result
    def calculate_expression(self, operator, num1, num2):
        if operator == '+':
            return int(num1) + int(num2)
        elif operator == '-':
            return int(num1) - int(num2)
        elif operator == '*':
            return int(num1) * int(num2)
        elif operator == '/':
            return int(num1) // int(num2)
        elif operator == '%':
            return int(num1) % int(num2)
        