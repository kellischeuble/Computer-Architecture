"""CPU functionality."""

import sys

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

        filename = sys.argv[1]

        with open(filename) as f:
            for address, line in enumerate(f):
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.memory[address] = v

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.stack_pointer,
            #self.fl,
            #self.ie,
            self.ram_read(self.stack_pointer),
            self.ram_read(self.stack_pointer + 1),
            self.ram_read(self.stack_pointer + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        while self.running:
            # self.trace()
            IR = self.ram_read(self.stack_pointer)
            opperand_a = self.ram_read(self.stack_pointer + 1)
            opperand_b = self.ram_read(self.stack_pointer + 2)

            if IR == HLT:
                self.running = False
            elif IR == LDI:
                self.registers[opperand_a] = opperand_b
                self.stack_pointer += 3
            elif IR == PRN:
                print(self.registers[opperand_a])
                self.stack_pointer += 2
            elif IR == MUL:
                product = self.registers[opperand_a] * self.registers[opperand_b]
                print(int(product))
                self.stack_pointer += 3
            else:
                print(f"Uknown instruction {IR} at address {self.stack_pointer}")
                self.stack_pointer += 1
