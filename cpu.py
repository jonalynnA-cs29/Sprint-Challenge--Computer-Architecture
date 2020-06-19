#CPU functionality.#

import sys
#www---www------------<<-=<<   ALU Operations  >>= ->>------------www---www#
HLT = 0b00000001
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
INC = 0b01100101
DEC = 0b01100110
CMP = 0b10100111
AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101
#www---www------------<<-=<<   PC Mutators   >>= ->>------------www---www#
CALL = 0b01010000
RET = 0b00010001
INT = 0b01010010
IRET = 0b00010011
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
JGT = 0b01010111
JLT = 0b01011000
JLE = 0b01011001
JGE = 0b01011010
#www---www------------<<-=<<   Other   >>= ->>------------www---www#
NOP = 0b00000000
LDI = 0b10000010
LD = 0b10000011
ST = 0b10000100
push = 0b01000101
pop = 0b01000110
PRN = 0b01000111
PRA = 0b01001000

# www---www------------<<-=<<   Flags   >>= ->>------------www---www#

# greater gtf == > flag, ltf == < flag, etf == = flag
ltf = 0b100
gtf = 0b010
etf = 0b001

SP = 7  # SP assign to be use R7 per spec


class CPU:
    #Main CPU class.#

    #www---www------------<<-=<<   Constructor   >>= ->>------------www---www#

    def __init__(self):
        #Construct a new CPU.#
        self.ram = [0] * 256  # this is our memory
        self.reg = [0] * 8
        self.pc = 0  # the Program Counter ~~ > index of the current instruction
        self.running = True  # a variable used to run our RUN repl
        self.flags = 0b00000001
        self.branch_table = {
            HLT: self.HLT_operation,
            LDI: self.LDI_operation,
            PRN: self.PRN_operation,
            ADD: self.ADD_operation,
            MUL: self.MUL_operation,
            push: self.PUSH_operation,
            pop: self.POP_operation,
            CALL: self.call_operation,
            RET: self.RET_operation,
            CMP: self.CMP_operation,
            JMP: self.JMP_operation,
            JEQ: self.JEQ_operation,
            JNE: self.JNE_operation
        }

#www---www------------<<-=<<    Methods   >>= ->>------------www---www#

    def HLT_operation(self, operand_a, operand_b):
        self.running = False

    def LDI_operation(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def PRN_operation(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def PUSH_operation(self, operand_a, operand_b):
        self.push(self.reg[operand_a])
        self.pc += 2

    def POP_operation(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop()
        self.pc += 2

    def ADD_operation(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)
        self.pc += 3

    def MUL_operation(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)
        self.pc += 3

#www---www------------<<-=<<    CALL|RET   >>= ->>------------www---www#

    def call_operation(self, operand_a, operand_b):
        self.reg[SP] -= 1  # decrement the SP
        self.ram[self.reg[SP]] = self.pc + 2
        update_reg = self.ram[self.pc + 1]
        self.pc = self.reg[update_reg]

    def RET_operation(self, operand_a, operand_b):
        self.pc = self.ram[self.reg[SP]]  # pop return MA off the stack
        self.reg[SP] += 1  # store popped MA in the PC

    def CMP_operation(self, operand_a, operand_b):  # compare the values in 2 registers
        self.alu('CMP', operand_a, operand_b)
        self.pc += 3

    def JEQ_operation(self, operand_a, operand_b):
        if self.flags & etf:  # If equal flag is set (true),
            # jump to the address stored in the given register
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def JMP_operation(self, operand_a, operand_b):
        # jump to the address stored in the given register
        self.pc = self.reg[operand_a]

    def JNE_operation(self, operand_a, operand_b):
        if not self.flags & etf:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

#www---www------------<<-=<<    Stack Functions   >>= ->>------------www---www#

    def push(self, value):
        self.reg[SP] -= 1
        self.ram_write(value, self.reg[7])

    def pop(self):
        value = self.ram_read(self.reg[7])
        self.reg[SP] += 1
        return value

#www---www------------<<-=<<   RAM Methods   >>= ->>------------www---www#

    def ram_read(self, address):  # Accept address to read and return the value stored there
        return self.ram[address]

    def ram_write(self, value, address):  # Accept a value to write and the address to write to
        self.ram[address] = value

#www---www------------<<-=<<   Load Methods   >>= ->>------------www---www#

    def load(self):
        #Load a program into memory.#
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                # Ignore comments
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == "":
                    continue  # Ignore blank lines
                instruction = int(num, 2)  # Convert Binary String to Number
                self.ram[address] = instruction
                address += 1

    def alu(self, operation, reg_a, reg_b):
        #ALU operations.#
        if operation == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif operation == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif operation == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags = ltf
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags = gtf
            else:
                self.flags = etf
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        #
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        #

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
        #Run the CPU.#
        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if int(bin(IR), 2) in self.branch_table:
                self.branch_table[IR](operand_a, operand_b)
            else:
                raise Exception(
                    f'Invalid {IR}, not in branch table \t {list(self.branch_table.keys())}')
