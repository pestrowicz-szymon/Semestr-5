class SymbolTable:
    def __init__(self):
        self.memory_offset = 0
        self.variables = dict()
        self.arrays = dict()
        self.procedures = []

    def __str__(self):
        s = ''
        for var_key in self.variables:
            var = self.variables[var_key]
            s += f'var {var_key} at address {var.address}\n'
        for arr_key in self.arrays:
            arr = self.arrays[arr_key]
            s += f'arr {arr_key} size {arr.size} at address {arr.address}\n'
        for proc in self.procedures:
            s += f'proc {proc.name}: return at address {proc.address}\n'
            for i in range(len(proc.args)):
                s += f'\targ {proc.args[i]} at address {proc.address + i + 1}\n'
        return s

    def put_variable(self, var, func_name='main'):
        var.address = self.memory_offset
        self.memory_offset += 1
        self.variables[f'{func_name}:{var.name}'] = var

    def put_array(self, arr, func_name='main'):
        arr.address = self.memory_offset
        self.memory_offset += arr.size
        self.arrays[f'{func_name}:{arr.name}'] = arr

    def put_procedure(self, proc):
        proc.address = self.memory_offset
        self.memory_offset += len(proc.args) + 1
        self.procedures += [proc]

    def get_variable_address(self, var_name, write, func_name='main'):
        name = f'{func_name}:{var_name}'
        if name not in self.variables:
            print(f'BŁĄD: brak zmiennej o nazwie \"{var_name}\" w funkcji \"{func_name}\"')
            exit(4)
        variable = self.variables[name]
        if not write and not variable.initialized:
            print(f'OSTRZEŻENIE: zmienna \"{var_name}\" jest niezainicjalizowana')
        if write:
            variable.initialized = True
        return variable.address

    def get_array_address(self, arr_name, func_name='main'):
        name = f'{func_name}:{arr_name}'
        if not name in self.arrays:
            print(f'BŁĄD: brak tablicy o nazwie \"{arr_name}\"')
            exit(4)
        array = self.arrays[name]
        return array.address

    def get_array_element_adr_const(self, arr_name, index, write, func_name='main'):
        name = f'{func_name}:{arr_name}'
        if name not in self.arrays:
            print(f'BŁĄD: brak tablicy o nazwie \"{arr_name}\"')
            exit(4)
        array = self.arrays[name]
        if not write and not array.initialized[index]:
            # print(f'BŁĄD: element nr {index} tablicy \"{arr_name}\" jest niezainicjalizowany')
            # exit(4)
            pass
        if index >= array.size:
            print(f'BŁĄD: element nr {index} jest poza zakresem tablicy \"{arr_name}\"')
            exit(4)
        if write:
            array.initialized[index] = True
        return array.address + index

    def get_procedure(self, proc_name, from_func='main'):
        for i in range(len(self.procedures)):
            if from_func == self.procedures[i].name:
                print(
                    f'BŁĄD: brak procedury o nazwie \"{proc_name}\" (lub nie można jej wywołać z procedury \"{from_func}\")')
                exit(4)
            elif proc_name == self.procedures[i].name:
                return self.procedures[i]
        print(f'BŁĄD: brak procedury o nazwie {proc_name}')
        exit(4)

    def get_procedure_parameter_address(self, param, proc_name):
        procedure = self.get_procedure(proc_name)
        if param == 'RET':
            return procedure.address
        #if param == 'FIRST':
        #    return procedure.address + 1
        i = procedure.address + 1
        for arg in procedure.args:
            if type(arg) is tuple:
                if arg[1] == param:
                    return i
            else:
                if arg == param:
                    return i
            i = i + 1
        print(f'BŁĄD: brak parametru o nazwie \"{param}\" w procedurze \"{proc_name}\"')
        exit(4)

    def is_variable(self, var_name, func_name='main'):
        name = f'{func_name}:{var_name}'
        return name in self.variables

    def is_array(self, arr_name, func_name='main'):
        name = f'{func_name}:{arr_name}'
        return name in self.arrays

    def is_param(self, param_name, proc_name):
        procedure = self.get_procedure(proc_name)
        for arg in procedure.args:
            if type(arg) is tuple:
                if arg[1] == param_name:
                    return True
            else:
                if arg == param_name:
                    return True
        return False