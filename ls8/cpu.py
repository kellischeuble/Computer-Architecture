"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.memory = [0] * 256
        self.registers = [0] * 8
        self.stack_pointer = 0

    def ram_read(self, MAR):
        """
        address: address to read
        returns value stored at that slot in memory
        """
        return self.memory[MAR]

    def ram_write(self, MDR, MAR):
        """
        value: value to write
        address: adress to write value to
        """
        self.memory[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram_read(self.pc)
            opperand_a = self.ram_read(self.pc + 1)
            opperand_b = self.ram_read(self.pc + 2)

        if IR == HLT:
            self.running = False
        elif IR == LDI:
            self.registers[opperand_a] = opperand_b
            self.stack_pointer += 3
        elif IR == PRN:
            print(self.registers[opperand_a])
            self.stack_pointer += 2
        else:
            print(f"Uknown instruction {IR} at address {self.stack_pointer}")
            # exit
