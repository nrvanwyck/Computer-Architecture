"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = self.reg[7]

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        program = []
        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                if len(line) > 0:
                    binary_string = line.split(" #")[0]
                    integer_value = int(binary_string, 2)
                    program.append(integer_value)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""

        ldi = 0b10000010
        prn = 0b01000111
        mul = 0b10100010
        hlt = 0b00000001
        push = 0b01000101
        pop = 0b01000110

        while True:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == ldi:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == prn:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == mul:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == push:
                self.ram_write(self.sp, self.reg[operand_a])
                self.pc += 2
                self.sp -= 1
            elif ir == pop:
                self.reg[operand_a] = self.ram_read(self.sp + 1)
                self.sp += 1
                self.pc += 2
            elif ir == hlt:
                break
            else:
                print(f"Invalid instruction. {self.ram[self.pc]}")
                sys.exit(1)
