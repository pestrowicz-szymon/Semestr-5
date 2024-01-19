from symbol_table import Variable


class CodeGenerator:
    def __init__(self, procedures, main, symbols):
        self.procedures = procedures
        self.main = main
        self.symbols = symbols
        self.code = []
        self.iterators = []

    def gen_code(self):
        self.gen_code_from_commands(self.procedures, self.main)
        self.code.append("HALT")

    def gen_code_from_commands(self, procedures, main):
        #for procedure in procedures:
        #    self.code.append(procedure)
        for code in main:
            if code[0] == 'read':
                self.code.append(f'READ')
                self.code.append(f'RST b')
                for i in range(self.symbols.get_address(code[1])):
                    self.code.append(f'INC b')
                self.code.append(f'STORE b')
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


                


        #for symbol in self.symbols:
        #    self.code.append(symbol)
        

    def gen_const(self, const, reg='a'):
        self.code.append(f"RESET {reg}")
        if const > 0:
            bits = bin(const)[2:]
            for bit in bits[:-1]:
                if bit == '1':
                    self.code.append(f"INC {reg}")
                self.code.append(f"SHL {reg}")
            if bits[-1] == '1':
                self.code.append(f"INC {reg}")

    def calculate_expression(self, expression, target_reg='a', second_reg='b', third_reg='c', fourth_reg='d',
                             fifth_reg='e'):
        if expression[0] == "const":
            self.gen_const(expression[1], target_reg)

        elif expression[0] == "load":
            if type(expression[1]) == tuple:
                if expression[1][0] == "undeclared":
                    self.load_variable(expression[1][1], target_reg, declared=False)
                elif expression[1][0] == "array":
                    self.load_array_at(expression[1][1], expression[1][2], target_reg, second_reg)
            else:
                if self.symbols[expression[1]].initialized:
                    self.load_variable(expression[1], target_reg)
                else:
                    raise Exception(f"Use of uninitialized variable {expression[1]}")

        else:
            if expression[1][0] == 'const':
                const, var = 1, 2
            elif expression[2][0] == 'const':
                const, var = 2, 1
            else:
                const = None

            if expression[0] == "add":
                if expression[1][0] == expression[2][0] == "const":
                    self.gen_const(expression[1][1] + expression[2][1], target_reg)

                elif expression[1] == expression[2]:
                    self.calculate_expression(expression[1], target_reg, second_reg)
                    self.code.append(f"SHL {target_reg}")

                elif const and expression[const][1] < 12:
                    self.calculate_expression(expression[var], target_reg, second_reg)
                    change = f"INC {target_reg}"
                    self.code += expression[const][1] * [change]

                else:
                    self.calculate_expression(expression[1], target_reg, second_reg)
                    self.calculate_expression(expression[2], second_reg, third_reg)
                    self.code.append(f"ADD {target_reg} {second_reg}")

            elif expression[0] == "sub":
                if expression[1][0] == expression[2][0] == "const":
                    val = max(0, expression[1][1] - expression[2][1])
                    if val:
                        self.gen_const(val, target_reg)
                    else:
                        self.code.append(f"RESET {target_reg}")

                elif expression[1] == expression[2]:
                    self.code.append(f"RESET {target_reg}")

                elif const and const == 2 and expression[const][1] < 12:
                    self.calculate_expression(expression[var], target_reg, second_reg)
                    change = f"DEC {target_reg}"
                    self.code += expression[const][1] * [change]

                elif const and const == 1 and expression[const][1] == 0:
                    self.code.append(f"RESET {target_reg}")

                else:
                    self.calculate_expression(expression[1], target_reg, second_reg)
                    self.calculate_expression(expression[2], second_reg, third_reg)
                    self.code.append(f"SUB {target_reg} {second_reg}")

            elif expression[0] == "mul":
                if expression[1][0] == expression[2][0] == "const":
                    self.gen_const(expression[1][1] * expression[2][1], target_reg)
                    return

                if const:
                    val = expression[const][1]
                    if val == 0:
                        self.code.append(f"RESET {target_reg}")
                        return
                    elif val == 1:
                        self.calculate_expression(expression[var], target_reg, second_reg)
                        return
                    elif val & (val - 1) == 0:
                        self.calculate_expression(expression[var], target_reg, second_reg)
                        while val > 1:
                            self.code.append(f"SHL {target_reg}")
                            val /= 2
                        return

                if expression[1] == expression[2]:
                    self.calculate_expression(expression[1], second_reg, target_reg)
                    self.code.append(f"RESET {third_reg}")
                    self.code.append(f"ADD {third_reg} {second_reg}")
                else:
                    self.calculate_expression(expression[1], second_reg, target_reg)
                    self.calculate_expression(expression[2], third_reg, target_reg)

                self.code.append(f"RESET {target_reg}")
                self.code.append(f"JZERO {second_reg} 21")
                self.code.append(f"JZERO {third_reg} 20")
                self.code.append(f"ADD {target_reg} {second_reg}")
                self.code.append(f"SUB {target_reg} {third_reg}")
                self.code.append(f"JZERO {target_reg} 9")

                # if second >= third it's better to do $2 * $3
                self.code.append(f"RESET {target_reg}")
                self.code.append(f"JZERO {third_reg} 15")
                self.code.append(f"JODD {third_reg} 2")
                self.code.append("JUMP 2")
                self.code.append(f"ADD {target_reg} {second_reg}")
                self.code.append(f"SHR {third_reg}")
                self.code.append(f"SHL {second_reg}")
                self.code.append("JUMP -6")

                # if second <= third it's better to do $3 * $2
                self.code.append(f"RESET {target_reg}")
                self.code.append(f"JZERO {second_reg} 7")
                self.code.append(f"JODD {second_reg} 2")
                self.code.append("JUMP 2")
                self.code.append(f"ADD {target_reg} {third_reg}")
                self.code.append(f"SHR {second_reg}")
                self.code.append(f"SHL {third_reg}")
                self.code.append("JUMP -6")

            elif expression[0] == "div":
                if expression[1][0] == expression[2][0] == "const":
                    if expression[2][1] > 0:
                        self.gen_const(expression[1][1] // expression[2][1], target_reg)
                    else:
                        self.code.append(f"RESET {target_reg}")
                    return

                elif expression[1] == expression[2]:
                    self.calculate_expression(expression[1], third_reg, second_reg)
                    self.code.append(f"RESET {target_reg}")
                    self.code.append(f"JZERO {third_reg} 2")
                    self.code.append(f"INC {target_reg}")
                    return

                elif const and const == 1 and expression[const][1] == 0:
                    self.code.append(f"RESET {target_reg}")
                    return

                elif const and const == 2:
                    val = expression[const][1]
                    if val == 0:
                        self.code.append(f"RESET {target_reg}")
                        return
                    elif val == 1:
                        self.calculate_expression(expression[var], target_reg, second_reg)
                        return
                    elif val & (val - 1) == 0:
                        self.calculate_expression(expression[var], target_reg, second_reg)
                        while val > 1:
                            self.code.append(f"SHR {target_reg}")
                            val /= 2
                        return

                self.calculate_expression(expression[1], third_reg, second_reg)
                self.calculate_expression(expression[2], fourth_reg, second_reg)
                self.perform_division(target_reg, second_reg, third_reg, fourth_reg, fifth_reg)

            elif expression[0] == "mod":
                if expression[1][0] == expression[2][0] == "const":
                    if expression[2][1] > 0:
                        self.gen_const(expression[1][1] % expression[2][1], target_reg)
                    else:
                        self.code.append(f"RESET {target_reg}")
                    return

                elif expression[1] == expression[2]:
                    self.code.append(f"RESET {target_reg}")
                    return

                elif const and const == 1 and expression[const][1] == 0:
                    self.code.append(f"RESET {target_reg}")
                    return

                elif const and const == 2:
                    val = expression[const][1]
                    if val < 2:
                        self.code.append(f"RESET {target_reg}")
                        return
                    elif val == 2:
                        self.calculate_expression(expression[var], second_reg, target_reg)
                        self.code.append(f"RESET {target_reg}")
                        self.code.append(f"JODD {second_reg} 2")
                        self.code.append(f"JUMP 2")
                        self.code.append(f"INC {target_reg}")
                        return

                self.calculate_expression(expression[1], third_reg, second_reg)
                self.calculate_expression(expression[2], fourth_reg, second_reg)
                self.perform_division(second_reg, target_reg, third_reg, fourth_reg, fifth_reg)

    def perform_division(self, quotient_register='a', remainder_register='b', dividend_register='c',
                         divisor_register='d', temp_register='e'):
        start = len(self.code)
        self.code.append(f"RESET {quotient_register}")
        self.code.append(f"RESET {remainder_register}")
        self.code.append(f"JZERO {divisor_register} finish")
        self.code.append(f"ADD {remainder_register} {dividend_register}")

        self.code.append(f"RESET {dividend_register}")
        self.code.append(f"ADD {dividend_register} {divisor_register}")
        self.code.append(f"RESET {temp_register}")
        self.code.append(f"ADD {temp_register} {remainder_register}")
        self.code.append(f"SUB {temp_register} {dividend_register}")
        self.code.append(f"JZERO {temp_register} block_start")
        self.code.append(f"RESET {temp_register}")
        self.code.append(f"ADD {temp_register} {dividend_register}")
        self.code.append(f"SUB {temp_register} {remainder_register}")
        self.code.append(f"JZERO {temp_register} 3")
        self.code.append(f"SHR {dividend_register}")
        self.code.append(f"JUMP 3")
        self.code.append(f"SHL {dividend_register}")
        self.code.append(f"JUMP -7")

        block_start = len(self.code)
        self.code.append(f"RESET {temp_register}")
        self.code.append(f"ADD {temp_register} {dividend_register}")
        self.code.append(f"SUB {temp_register} {remainder_register}")
        self.code.append(f"JZERO {temp_register} 2")
        self.code.append(f"JUMP finish")
        self.code.append(f"SUB {remainder_register} {dividend_register}")
        self.code.append(f"INC {quotient_register}")

        midblock_start = len(self.code)
        self.code.append(f"RESET {temp_register}")
        self.code.append(f"ADD {temp_register} {dividend_register}")
        self.code.append(f"SUB {temp_register} {remainder_register}")
        self.code.append(f"JZERO {temp_register} block_start")
        self.code.append(f"SHR {dividend_register}")
        self.code.append(f"RESET {temp_register}")
        self.code.append(f"ADD {temp_register} {divisor_register}")
        self.code.append(f"SUB {temp_register} {dividend_register}")
        self.code.append(f"JZERO {temp_register} 2")
        self.code.append(f"JUMP finish")
        self.code.append(f"SHL {quotient_register}")
        self.code.append(f"JUMP midblock_start")
        end = len(self.code)

        for i in range(start, end):
            self.code[i] = self.code[i].replace('midblock_start', str(midblock_start - i))
            self.code[i] = self.code[i].replace('block_start', str(block_start - i))
            self.code[i] = self.code[i].replace('finish', str(end - i))

    def simplify_condition(self, condition):
        if condition[1][0] == "const" and condition[2][0] == "const":
            if condition[0] == "le":
                return condition[1][1] <= condition[2][1]
            elif condition[0] == "ge":
                return condition[1][1] >= condition[2][1]
            elif condition[0] == "lt":
                return condition[1][1] < condition[2][1]
            elif condition[0] == "gt":
                return condition[1][1] > condition[2][1]
            elif condition[0] == "eq":
                return condition[1][1] == condition[2][1]
            elif condition[0] == "ne":
                return condition[1][1] != condition[2][1]

        elif condition[1][0] == "const" and condition[1][1] == 0:
            if condition[0] == "le":
                return True
            elif condition[0] == "gt":
                return False
            else:
                return condition

        elif condition[2][0] == "const" and condition[2][1] == 0:
            if condition[0] == "ge":
                return True
            elif condition[0] == "lt":
                return False
            else:
                return condition

        elif condition[1] == condition[2]:
            if condition[0] in ["ge", "le", "eq"]:
                return True
            else:
                return False

        else:
            return condition

    def check_condition(self, condition, first_reg='a', second_reg='b', third_reg='c'):
        if condition[1][0] == "const" and condition[1][1] == 0:
            if condition[0] == "ge" or condition[0] == "eq":
                self.calculate_expression(condition[2], first_reg, second_reg)
                self.code.append(f"JZERO {first_reg} 2")
                self.code.append("JUMP finish")

            elif condition[0] == "lt" or condition[0] == "ne":
                self.calculate_expression(condition[2], first_reg, second_reg)
                self.code.append(f"JZERO {first_reg} finish")

        elif condition[2][0] == "const" and condition[2][1] == 0:
            if condition[0] == "le" or condition[0] == "eq":
                self.calculate_expression(condition[1], first_reg, second_reg)
                self.code.append(f"JZERO {first_reg} 2")
                self.code.append("JUMP finish")

            elif condition[0] == "gt" or condition[0] == "ne":
                self.calculate_expression(condition[1], first_reg, second_reg)
                self.code.append(f"JZERO {first_reg} finish")

        else:
            self.calculate_expression(condition[1], first_reg, third_reg)
            self.calculate_expression(condition[2], second_reg, third_reg)

            if condition[0] == "le":
                self.code.append(f"SUB {first_reg} {second_reg}")
                self.code.append(f"JZERO {first_reg} 2")
                self.code.append(f"JUMP finish")

            elif condition[0] == "ge":
                self.code.append(f"SUB {second_reg} {first_reg}")
                self.code.append(f"JZERO {second_reg} 2")
                self.code.append(f"JUMP finish")

            elif condition[0] == "lt":
                self.code.append(f"SUB {second_reg} {first_reg}")
                self.code.append(f"JZERO {second_reg} finish")

            elif condition[0] == "gt":
                self.code.append(f"SUB {first_reg} {second_reg}")
                self.code.append(f"JZERO {first_reg} finish")

            elif condition[0] == "eq":
                self.code.append(f"RESET {third_reg}")
                self.code.append(f"ADD {third_reg} {first_reg}")
                self.code.append(f"SUB {first_reg} {second_reg}")
                self.code.append(f"JZERO {first_reg} 2")
                self.code.append(f"JUMP finish")
                self.code.append(f"SUB {second_reg} {third_reg}")
                self.code.append(f"JZERO {second_reg} 2")
                self.code.append(f"JUMP finish")

            elif condition[0] == "ne":
                self.code.append(f"RESET {third_reg}")
                self.code.append(f"ADD {third_reg} {first_reg}")
                self.code.append(f"SUB {first_reg} {second_reg}")
                self.code.append(f"JZERO {first_reg} 2")
                self.code.append(f"JUMP 3")
                self.code.append(f"SUB {second_reg} {third_reg}")
                self.code.append(f"JZERO {second_reg} finish")

    def load_array_at(self, array, index, reg1, reg2):
        self.load_array_address_at(array, index, reg1, reg2)
        self.code.append(f"LOAD {reg1} {reg1}")

    def load_array_address_at(self, array, index, reg1, reg2):
        if type(index) == int:
            address = self.symbols.get_address((array, index))
            self.gen_const(address, reg1)
        elif type(index) == tuple:
            if type(index[1]) == tuple:
                self.load_variable(index[1][1], reg1, declared=False)
            else:
                if not self.symbols[index[1]].initialized:
                    raise Exception(f"Trying to use {array}({index[1]}) where variable {index[1]} is uninitialized")
                self.load_variable(index[1], reg1)
            var = self.symbols.get_variable(array)
            self.gen_const(var.first_index, reg2)
            self.code.append(f"SUB {reg1} {reg2}")
            self.gen_const(var.memory_offset, reg2)
            self.code.append(f"ADD {reg1} {reg2}")

    def load_variable(self, name, reg, declared=True):
        if not declared and self.iterators and name == self.iterators[-1]:
            self.code.append(f"RESET {reg}")
            self.code.append(f"ADD {reg} f")
        else:
            self.load_variable_address(name, reg, declared)
            self.code.append(f"LOAD {reg} {reg}")

    def load_variable_address(self, name, reg, declared=True):
        if declared or name in self.iterators:
            address = self.symbols.get_address(name)
            self.gen_const(address, reg)
            if self.iterators and name == self.iterators[-1]:
                self.code.append(f"STORE f {reg}")
        else:
            raise Exception(f"Undeclared variable {name}")

    def prepare_consts_before_block(self, consts, reg1='a', reg2='b'):
        for c in consts:
            address = self.symbols.get_const(c)
            if address is None:
                address = self.symbols.add_const(c)
                self.gen_const(address, reg1)
                self.gen_const(c, reg2)
                self.code.append(f"STORE {reg2} {reg1}")