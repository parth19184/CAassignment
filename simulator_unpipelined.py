from typing import List
import numpy as np
import time
        
register_dict = {
    "00000":'R0',
    "00001":'R1',
    "00010":'R2',
    "00011":'R3',
    "00100":'R4',
    "00101":'R5',
    "00110":'R6',
    "00111":'R7',
    "01000":'R8',
    "01001":'R9',
    "01010":'R10',
    "01011":'R11',
    "01100":'R12',
    "01101":'R13',
    "01110":'R14',
    "01111":'R15',
    "10000":'R16',
    "10001":'R17',
    "10010":'R18',
    "10011":'R19',
    "10100":'R20',
    "10101":'R21',
    "10110":'R22',
    "10111":'R23',
    "11000":'R24',
    "11001":'R25',
    "11010":'R26',
    "11011":'R27',
    "11100":'R28',
    "11101":'R29',
    "11110":'R30',
    "11111":'R31'
}
type_dict = {
    "add": "01100",
    "addi": "00100",
    "sub": "01100",
    "lw": "00000",
    "sw": "01000",
    "jalr": "11001",
    "jal": "11011",
    "beq": "11000",
    "bne": "11000",
    "blt": "11000",
    "bge": "11000",
    "lui": "01101",
    "and": "01100",
    "or": "01100",
    "xor": "01100",
    "sll": "01100",
    "sra": "01100"
}
RF = {
    'R0':0,
    'R1':0,
    'R2':0,
    'R3':0,
    'R4':0,
    'R5':0,
    'R6':0,
    'R7':0,
    'R8':0,
    'R9':0,
    'R10':0,
    'R11':0,
    'R12':0,
    'R13':0,
    'R14':0,
    'R15':0,
    'R16':0,
    'R17':0,
    'R18':0,
    'R19':0,
    'R20':0,
    'R21':0,
    'R22':0,
    'R23':0,
    'R24':0,
    'R25':0,
    'R26':0,
    'R27':0,
    'R28':0,
    'R29':0,
    'R30':0,
    'R31':0
}

class Mem : 
    def __init__(self, size = 256, access_time = 1):
        self.bits = 32
        self.size = size
        self.access_time = access_time
        self.memory = []
    
    def initialize(self):
        i = 0
        with open('sample_binary.txt') as b:
            lines = b.readlines()
            # print(lines)
            for line in lines:
                self.memory.append(line)
                i+=1
        ctr = i
        while(ctr<=self.size):
            self.memory.append("0")
            ctr+=1
        return i
    
    def getData(self,row):
        return self.memory[row]
    
    def setData(self,row,data):
        self.memory[row]=data

    def dump(self):
        print(self.memory)


class EE:
    def __init__(self,mem):
        self.instruc = 0
        self.mem = mem
    
    def execute(self,instruc,PC):
        # fetch
        self.instruc = instruc
        
        # decode
        opcode = self.instruc[25:30]
        rs2 = register_dict[self.instruc[7:12]]
        rs1 = register_dict[self.instruc[12:17]]
        rd = register_dict[self.instruc[20:25]]

        # arithmetic instructions
        if(opcode=="01100"):
            # add,sub,or,and,xor,sll,sra
            op1 = RF[rs1]
            op2 = RF[rs2]

            funct3 = self.instruc[17:20]
            if(self.instruc[0:5]=="00000"):
                if(funct3=="000"):
                    RF[rd] = op1 + op2
                elif(funct3=="110"):
                    # or
                    RF[rd] = op1 | op2
                elif(funct3=="111"):
                    # and
                    RF[rd] = op1 & op2
                elif(funct3=="100"):
                    # xor
                    RF[rd] = op1 ^ op2
                elif(funct3=="001"):
                    # sll
                    RF[rd] = op1 << op2
            else:
                if(funct3=="000"):
                    # subtract
                    RF[rd] = op1-op2
                elif(funct3=="101"):
                    # sra
                    RF[rd] = op1 >> op2
            
            PC+=1
        
        # add immediate
        elif(opcode=="00100"):
            op1 = RF[rs1]
            imm = int(self.instruc[0:12],2)
            RF[rd] = op1 + imm
            PC+=1

        # load upper immediate
        elif(opcode=="01101"):
            imm = self.instruc[0:20]
            imm+="000000000000"
            RF[rd] = int(imm,2)
            PC+=1

        # branches
        # unconditional branches
        elif(opcode == "11011"):
            # jal
            offset = self.instruc[0]+self.instruc[12:20]+self.instruc[11]+self.instruc[1:11]
            offset = int(offset,2)
            RF[rd] = PC+1
            PC+=offset
        elif(opcode == "11001"):
            # jalr
            offset = int(self.instruc[0:12],2)
            op1 = RF[rs1]
            RF[rd] = PC+1            
            PC=(op1+offset)
            PC = '{:032b}'.format(PC)[0:31] + '0'
            PC = int(PC,2)
        
        # conditional branches
        elif(opcode == "11000"):
            offset = self.instruc[0]+self.instruc[24]+self.instruc[1:7]+self.instruc[20:24]
            offset = int(offset,2)
            op1 = RF[rs1]
            op2 = RF[rs2]
            funct3 = self.instruc[17:20]

            if(funct3=="000"):
                # BEQ
                if(RF[rs1]==RF[rs2]):
                    PC=offset
                else: PC+=1

            elif(funct3=="001"):
                # BNE
                if(RF[rs1]!=RF[rs2]):
                    PC=offset
                else: PC+=1

            elif(funct3=="100"):
                # BLT
                if(RF[rs1]<RF[rs2]):
                    PC=offset
                else: PC+=1

            elif(funct3=="101"):
                # BGE
                if(RF[rs1]>=RF[rs2]):
                    PC=offset
                else: PC+=1
        # load
        elif(opcode=="00000"):
            offset = int(self.instruc[0:12],2)
            op1 = RF[rs1]
            RF[rd] = int(self.mem.getData(op1+offset),2)
            PC+=1
        
        # store
        elif(opcode=="01000"):
            offset = int(self.instruc[0:7]+self.instruc[20:25],2)
            op1 = RF[rs1]
            op2 = RF[rs2]
            val = '{:032b}'.format(op2)
            self.mem.setData(op1+offset,val)
            PC+=1
        else: PC+=1

        return PC

def main():
    MEM = Mem()    
    EX = EE(MEM)
    PC = 0
    halted = False

    # initializing memory
    no_of_instructions = MEM.initialize()
    MEM.dump()

    while(not halted):
        # start timer
        tic = time.perf_counter_ns()
        # Fetch instruction from memory
        instruc = MEM.getData(PC)
        # execute the instruction
        PC = EX.execute(instruc,PC)
        # stop the timer
        toc = time.perf_counter_ns()
        # Check if program execution is finished
        if(PC>=no_of_instructions): 
            halted = True
        print(PC)
        # printing the register file
        print(RF)   
        # printing the time taken (in ns) to process the instruction
        print(f"Instruction Execution completed in {toc-tic:0.4f} nanoseconds")
    
    # printing the memory state at the end of the execution
    MEM.dump()

if __name__ == "__main__":
    main()