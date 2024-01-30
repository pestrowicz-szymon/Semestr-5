from enum import Enum

class DataType(Enum):
    VARIABLE = 1
    ARRAY = 2
    PROCEDURE = 3

class SymbolTable:
    def __init__(self):
        self.memory_offset = 0
        self.variables = dict()
        self.arrays = dict()
        self.procedures = []
    
    def put(self, data, type, func_name='main'):
        data.address = self.memory_offset
        if type == DataType.VARIABLE:
            self.memory_offset += 1
            self.variables[f'{func_name}>{data.name}'] = data
        if type == DataType.ARRAY:
            self.memory_offset += data.size
            self.arrays[f'{func_name}>{data.name}'] = data
        if type == DataType.PROCEDURE:
            self.memory_offset += len(data.args) + 1
            self.procedures += [data]

    def get_variable_address(self, var_name, is_initialized, func_name='main'):
        name = f'{func_name}>{var_name}'
        if name not in self.variables:
            print(f'Error: name not recognized \"{var_name}\"')
            exit(4)
        variable = self.variables[name]
        if not is_initialized and not variable.initialized:
            print(f'Warning: \"{var_name}\" may not be initialized')
        if is_initialized:
            variable.initialized = True
        return variable.address

    def get_array_address(self, arr_name, func_name='main'):
        name = f'{func_name}>{arr_name}'
        if not name in self.arrays:
            print(f'Error: name not recognized \"{arr_name}\"')
            exit(4)
        array = self.arrays[name]
        return array.address

    def get_array_element_adr_const(self, arr_name, index, write, func_name='main'):
        name = f'{func_name}>{arr_name}'
        if name not in self.arrays:
            print(f'Error: name not recognized \"{arr_name}\"')
            exit(4)
        array = self.arrays[name]
        if not write and not array.initialized[index]:
            pass
        if index >= array.size:
            print(f'Error: array \"{arr_name}\" is smaller than {index}')
            exit(4)
        if write:
            array.initialized[index] = True
        return array.address + index

    def get_procedure(self, proc_name, from_func='main'):
        for i in range(len(self.procedures)):
            if from_func == self.procedures[i].name:
                print(
                    f'Error: procedure unknown \"{proc_name}\"')
                exit(4)
            elif proc_name == self.procedures[i].name:
                return self.procedures[i]
        raise Exception('ex')

    def get_procedure_parameter_address(self, param, proc_name):
        procedure = self.get_procedure(proc_name)
        if param == 'RET':
            return procedure.address
        i = procedure.address + 1
        for arg in procedure.args:
            if type(arg) is tuple:
                if arg[1] == param:
                    return i
            else:
                if arg == param:
                    return i
            i = i + 1
        print(f'Error: name not recognized \"{param}\"')
        exit(4)

    def is_variable(self, var_name, func_name='main'):
        name = f'{func_name}>{var_name}'
        return name in self.variables

    def is_array(self, arr_name, func_name='main'):
        name = f'{func_name}>{arr_name}'
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