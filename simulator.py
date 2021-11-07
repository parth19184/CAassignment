# class Mem : 
# Methods: write(data,addr), read(addr), initialize()
# Attribute: bits = 32, size =  256, access time = ?

from typing import List


class Mem : 
    def __init__(self, size = 256, access_time = 1):
        self.bits = 32
        self.size = size
        self.access_time = access_time
        self.memory = list()
    
    def initialize(self):
        with open('binary.txt') as b:
            for line in b:
                self.memory.append(line)
    
    def getData(self,row):
        return self.memory[row]

    def dump(self):
        print(self.memory)
        

PC = 0
RF = []


register_dict = {
    "00000":0,
    "00001":1,
    "00010":2,
    "00011":3,
    "00100":4,
    "00101":5,
    "00110":6,
    "00111":7,
    "01000":8,
    "01001":9,
    "01010":10,
    "01011":11,
    "01100":12,
    "01101":13,
    "01110":14,
    "01111":15,
    "10000":16,
    "10001":17,
    "10010":18,
    "10011":19,
    "10100":20,
    "10101":21,
    "10110":22,
    "10111":23,
    "11000":24,
    "11001":25,
    "11010":26,
    "11011":27,
    "11100":28,
    "11101":29,
    "11110":30,
    "11111":31,
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

class EE:
    def __init__(self):
        self.F = Fetch()
        self.D = Decode()
        self.X = Execute()
        self.M = Memory()
        self.W = WriteBack()

    def execute(self):
        self.F.execute(PC)
        self.D.execute(self.F,PC)
        self.X.execute(self.D,PC)
        self.M.execute(self.X)
        self.W.execute(self.M)

class Fetch:
    def __init__(self):
        self.instruc = 0
    
    def execute(self,PC,D):
        self.fetch(PC)

    def fetch(self,PC,mem):
        self.instruc = mem.getData(PC)

    def sendToDecode(self,D):
        return self.instruc

class Decode:
    def __init__(self):
        self.instruc = 0
        self.rd = 0
        self.rs1 = 0
        self.rs2 = 0
        self.offset = 0
        self.imm = 0
        self.op1 = 0
        self.op2 = 0
        self.F = 0
    
    def decode(self,PC):
        if(self.instruc[25:29]=="01100"):
            # add,sub,or,and,xor,sll,sra
            self.op1 = RF[self.rs1]
            self.op2 = RF[self.rs2]
        elif(self.instruc[25:29]=="11000"):
            # conditional branches beq,bnw,bge,blt
            self.offset = self.instruc[0]+self.instruc[24]+self.instruc[1:7]+self.instruc[20:24]
            self.offset = int(self.offset,2)
            self.op1 = RF[self.rs1]
            self.op2 = RF[self.rs2]
        elif(self.instruc[25:29]=="00000"):
            # load instruction
            self.offset = int(self.instruc[0:12],2)
            self.op1 = RF[self.rs1]
        elif(self.instruc[25:29]=="01000"):
            # store instruction
            self.offset = int(self.instruc[0:7]+self.instruc[20:25],2)
            self.op1 = RF[self.rs1]
            self.op2 = RF[self.rs2]
        elif(self.instruc[25:29]=="00100"):
            # add immediate(addi)
            self.op1 = RF[self.rs1]
            self.imm = int(self.instruc[0:12],2)
        elif(self.instruc[25:29] == "11001"):
            # jalr
            self.offset = self.instruc[0:12]
            self.op1 = RF[self.rs1]
            RF[self.rd] = PC+4            
            PC+=(self.op1+self.offset)&(0)
        else:
            # jal
            self.offset = self.instruc[0]+self.instruc[12:20]+self.instruc[11]+self.instruc[1:11]
            self.offset = int(self.offset,2)
            self.op1 = RF[self.rd] 
    
    def execute(self,F,PC):
        self.instruc = F.sendToDecode()
        self.rs2 = register_dict[self.instruc[7:12]]
        self.rs1 = register_dict[self.instruc[12:17]]
        self.rd = register_dict[self.instruc[20:25]]
        self.decode(PC)

    def sendToExecute(self):
        return (self.instruc, self.op1, self.op2, self.imm, self.offset, self.rd)

class Execute:
    def __init__(self):
        self.instruc = 0
        self.op1 = 0
        self.op2 = 0
        self.imm = 0
        self.offset = 0
        self.rd = 0
        self.res = 0
    
    def execute(self,D,PC):
        (self.instruc, self.op1, self.op2, self.imm, self.offset, self.rd) = D.sendToExecute()
        self.compute(PC)

    def compute(self,PC):
        if(self.instruc[25:29]=="01100"):
            # arithmetic instructions
            if(self.instruc[0:5]=="00000"):
                # add
                self.res = self.op1+self.op2
            elif(self.instruc[0:5]=="01000"):
                if(self.instruc[17:20]=="000"):
                    # subtract
                    self.res = self.op1-self.op2
                elif(self.instruc[17:20]=="101"):
                    # sra
                    self.res =  self.op1 >> self.op2
            elif(self.instruc[17:20]=="110"):
                # or
                self.res = self.op1 | self.op2
            elif(self.instruc[17:20]=="111"):
                # and
                self.res = self.op1 & self.op2
            elif(self.instruc[17:20]=="100"):
                # xor
                self.res = self.op1 ^ self.op2
            elif(self.instruc[17:20]=="001"):
                # sll
                self.res = self.op1 << self.op2
        
        elif(self.instruc[25:29]=="11000"):
            # conditional branches
            if(self.instruc[17:20]=="000"):
                # BEQ
                if(RF[self.rs1]==RF[self.rs2]):
                    PC+=self.offset

            elif(self.instruc[17:20]=="001"):
                # BNE
                if(RF[self.rs1]!=RF[self.rs2]):
                    PC+=self.offset

            elif(self.instruc[17:20]=="100"):
                # BLT
                if(RF[self.rs1]<RF[self.rs2]):
                    PC+=self.offset

            elif(self.instruc[17:20]=="101"):
                # BGE
                if(RF[self.rs1]>=RF[self.rs2]):
                    PC+=self.offset
        
        elif(self.instruc[25:29]=="00100"):
            # add immediate
                self.res = self.op1 + self.imm
        
        elif(self.instruc[25:29]=="01000"):
            # store
            self.res = self.op1 + self.offset
        
        elif(self.instruc[25:29]=="00000"):
            # load
            self.res = self.op1 + self.offset

    def sendToMemory(self):
        return (self.instruc,self.res,self.rd,self.op2)

class Memory:
    def __init__(self):
        self.instruc = 0
        self.rd = 0
        self.res = 0
        self.loadval = 0
        self.op2 = 0
    def execute(self,X):
        (self.instruc,self.res,self.rd,self.op2) = X.sendToMemory()
        if(self.instruc[25:29]=="01000"):
            # store
            RF[self.res] = self.op2
        elif(self.instruc[25:29]=="00000"):
            # load
            self.loadval = RF[self.res]
        
class WriteBack:
    pass

# pipelined approach using queue, bypassing, stalling to be implemented to address structural,data and control hazards

# class EE : 

# class Fetch: fetch(), updatePC(), stall()
# class Decode: extractData(), inputControl(), sendData()
# class Execute: performOperation()
# class Memory: read(), write() 
# class WriteBack: writeToRF()

# class CU: generateControl()