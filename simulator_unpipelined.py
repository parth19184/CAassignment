from typing import List
import numpy as np
        
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
        self.memory = np.full(size,"")
    
    def initialize(self):
        with open('binary.txt') as b:
            i = 0
            for line in b:
                self.memory[i]=line
                i+=1
    
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
    
    def execute(self,PC):
        # fetch
        self.instruc = self.mem.getData(PC)
        
        # decode
        opcode = self.instruc[25:29]
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
        if(opcode=="00100"):
            op1 = RF[rs1]
            imm = int(self.instruc[0:12],2)
            RF[rd] = op1 + imm
            PC+=1

        # load upper immediate
        if(opcode=="01101"):
            imm = self.instruc[0:20]
            imm+="000000000000"
            RF[rd] = int(imm,2)
            PC+=1

        # branches
        # unconditional branches
        if(opcode == "11011"):
            # jal
            offset = self.instruc[0]+self.instruc[12:20]+self.instruc[11]+self.instruc[1:11]
            offset = int(offset,2)
            RF[rd] = PC+1
            PC+=offset
        if(opcode == "11001"):
            # jalr
            offset = int(self.instruc[0:12],2)
            op1 = RF[rs1]
            RF[rd] = PC+1            
            PC+=(op1+offset)&(0)
        
        # conditional branches
        if(opcode == "11000"):
            offset = self.instruc[0]+self.instruc[24]+self.instruc[1:7]+self.instruc[20:24]
            offset = int(self.offset,2)
            op1 = RF[rs1]
            op2 = RF[rs2]
            funct3 = self.instruc[17:20]

            if(funct3=="000"):
                # BEQ
                if(RF[rs1]==RF[rs2]):
                    PC+=offset

            elif(funct3=="001"):
                # BNE
                if(RF[rs1]!=RF[rs2]):
                    PC+=offset

            elif(funct3=="100"):
                # BLT
                if(RF[rs1]<RF[rs2]):
                    PC+=offset

            elif(funct3=="101"):
                # BGE
                if(RF[rs1]>=RF[rs2]):
                    PC+=offset
        # load
        if(opcode=="00000"):
            offset = int(self.instruc[0:12],2)
            op1 = RF[rs1]
            RF[rd] = int(self.mem.getData(op1+offset),2)
            PC+=1
        
        # store
        if(opcode=="01000"):
            offset = int(self.instruc[0:7]+self.instruc[20:25],2)
            op1 = RF[rs1]
            op2 = RF[rs2]
            val = '{:032b}'.format(op2)
            self.mem.setData(op1+offset,val)
            PC+=1

PC = 0
def main():
    MEM = Mem()    
    EX = EE(MEM)
    halted = False

    # initializing memory
    MEM.initialize()
    