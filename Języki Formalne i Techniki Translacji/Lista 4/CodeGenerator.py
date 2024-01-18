import sys, enum

class Command(enum.Enum):
    PROGRAM_HALT = 1
    PROCEDURES_VAR = 2
    PROCEDURES = 3
    PROCEDURES_EMPTY = 4
    MAIN = 5
    MAIN_VAR = 6
    COMMANDS_COMMAND = 7
    COMMANDS = 8
    COMMAND_ASSIGN = 9
    COMMAND_IF = 10
    COMMAND_IF_ELSE = 11
    COMMAND_WHILE = 12
    COMMAND_REPEAT = 13
    COMMAND_PROC_CALL = 14
    COMMAND_READ = 15
    COMMAND_WRITE = 16
    

class Code:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class CodeGenerator:
    def __init__(self):
        self.procedure_addresses = {}


    def generate_code(self, code, param):
        return {
            Command.PROGRAM_HALT: lambda x: self.__program_halt(x),
            Command.PROCEDURES_VAR: lambda x: self.__procedures(x),
            Command.PROCEDURES: lambda x: self.__procedures(x),
            Command.PROCEDURES_EMPTY: lambda x: self.__procedures(x),
            Command.MAIN: lambda x: self.__main(x),
            Command.MAIN_VAR: lambda x: self.__main(x),
            Command.COMMANDS_COMMAND: lambda x: self.__commands_command(x),
            Command.COMMANDS: lambda x: self.__commands(x),
            Command.COMMAND_ASSIGN: lambda x: self.__command_assign(x),
            Command.COMMAND_IF: lambda x: self.__command_if(x),
            Command.COMMAND_IF_ELSE: lambda x: self.__command_if_else(x),
            Command.COMMAND_WHILE: lambda x: self.__command_while(x),
            Command.COMMAND_REPEAT: lambda x: self.__command_repeat(x),
            Command.COMMAND_PROC_CALL: lambda x: self.__command_proc_call(x),
            Command.COMMAND_READ: lambda x: self.__command_read(x),
            Command.COMMAND_WRITE: lambda x: self.__command_write(x),

        }[code](param)
    
    def __program_halt(self, x):
        procedures_codelength = len(x[0])
        strings = [str(Code(f'JUMP {procedures_codelength+1}'))]
        codes = []
        codes += x[0]
        codes += x[1]
        for code in codes:
            string = str(code)
            strings += [string]
        strings += ["HALT"]
        return strings
    
    def __procedures(self, x):
        previous_procedures = x[0]
        proc_head = x[1]
        proc_commands = x[2]
        self.procedure_addresses[proc_head]=len(previous_procedures)+1
        commands=[]
        for code in proc_commands:
            commands += ["COMMAND"]
        return commands
    
    def __main(self, x):
        codes = x[1]
        return codes
    
    #@TODO write functions for 'commands' and 'command

    def __commands_command(self, x):
        return []
    
    def __commands(self, x):
        return []
    
    def __command_(self, x):
        return []
    
    def __command_assign(self, x):
        return []
    
    def __command_if(self, x):
        return []
    
    def __command_if_else(self, x):
        return []
    
    def __command_while(self, x):
        return []
    
    def __command_repeat(self, x):
        return []
    
    def __command_proc_call(self, x):
        return []
    
    def __command_read(self, x):
        return []
    
    def __command_write(x):
        return []
