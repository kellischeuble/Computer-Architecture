"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xf4
        self.reg[7] = self.sp

        self.branchtable = {
            LDI: self.handleLDI,
            PRN: self.handlePRN,
            HLT: self.handleHLT,
            MUL: self.handleMUL,
            PSH: self.handlePUSH,
            POP: self.handlePOP,
            CALL: self.handleCALL,
            RET: self.handleRET,
        }

    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]

        if filename:
            with open(filename) as f:
                for address, line in enumerate(f):
                    line = line.split("#")
                    try:
                        v = int(line[0], 2)
                    except ValueError:
                        continue
                    self.ram[address] = v
        else:
            print('missing command line argument')
            sys.exit(0)

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handleHLT(self, a=None, b=None):
        self.running = False

    def handleLDI(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def handlePRN(self, a, b=None):
        print(self.reg[a])
        self.pc += 2

    def handleMUL(self, a, b):
        self.reg[a] = self.reg[a] * self.reg[b]
        self.pc += 3

    def handlePUSH(self, opperand_a, opperand_b):
        self.sp -= 1
        self.sp &= 0xff 

        reg_num = self.ram[self.pc + 1]
        val = self.reg[reg_num]

        self.ram[self.sp] = val
        self.pc += 2

    def handlePOP(self, opperand_a, opperand_b):
        val = self.ram[self.sp]
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = val
        self.sp += 1
        self.sp &= 0xff  # keep in range of 00-FF

        self.pc += 2

    def handleCALL(self, a, b):
        rc = self.pc + 2
        self.sp -= 1
        self.ram[self.sp] = rc

        self.pc = self.reg[a]

    def handleRET(self, a, b):
        val = self.ram[self.sp]
        self.pc = val
        self.sp += 1

    def handleADD(self, a, b):
        self.alu('ADD', a, b)
        self.pc += 3


    def run(self):
        """Run the CPU."""

        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR not in self.branchtable:
                print(f'unknown instruction {IR} at address {self.pc}')
                self.running=False
            else:
                f = self.branchtable[IR]
                f(operand_a, operand_b)