

from staq.stack import Stack, StackFrame, StackCell 
from staq.function import Function, FunctionArgument
from staq.archs.architecture import Architecture, Register
from typing import List
from cliify import commandParser, command

import re

@commandParser
class X86_cdecl(Architecture):
    def __init__(self, session = None, stack = None):
        super().__init__('cdecl', session=session, stack=stack)
        self.endian = 'little'


        self.registers = {
            'eax': Register('eax', 4, 'Return Value'),
            'ecx': Register('ecx', 4, 'Arg 1'),
            'edx': Register('edx', 4, 'Arg 2'),
            'ebx': Register('ebx', 4, 'Arg 3'),
            'esp': Register('esp', 4, 'Stack Pointer'),
            'ebp': Register('ebp', 4, 'Base Pointer'),
            'esi': Register('esi', 4, 'Source Index'),
            'edi': Register('edi', 4, 'Destination Index'),
            'eip': Register('eip', 4, 'Instruction Pointer')
        }

        self.setReg('esp', hex(self.stack.pointer))
        self.setReg('eip', '???')
        self.setReg('ebp', hex(self.stack.baseAddress))

    def clear(self):

        for key in self.registers:
            self.registers[key].value = None
        
        self.setReg('esp', hex(self.stack.pointer))
        self.setReg('eip', '???')
        self.setReg('ebp', hex(self.stack.baseAddress))



    def setInstructionPointer(self, val):

        self.setReg("eip", val)

    def setFramePointer(self, val):
        self.setReg("ebp", val)

    def setReturnValue(self, val):
        self.setReg("eax", val)
    
    
    


        