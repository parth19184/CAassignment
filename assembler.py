from typing import Counter
import numpy as np
import sys

class PC:
    instruction_mem = 0
    count = 0

#all registers from R0 to R31 with their binary strings
register_dict = {
    "R0":"00000",
    "R1":"00001",
    "R2":"00010",
    "R3":"00011",
    "R4":"00100",
    "R5":"00101",
    "R6":"00110",
    "R7":"00111",
    "R8":"01000",
    "R9":"01001",
    "R10":"01010",
    "R11":"01011",
    "R12":"01100",
    "R13":"01101",
    "R14":"01110",
    "R15":"01111",
    "R16":"10000",
    "R17":"10001",
    "R18":"10010",
    "R19":"10011",
    "R20":"10100",
    "R21":"10101",
    "R22":"10110",
    "R23":"10111",
    "R24":"11000",
    "R25":"11001",
    "R26":"11010",
    "R27":"11011",
    "R28":"11100",
    "R29":"11101",
    "R30":"11110",
    "R31":"11111"

}
def init_reg_file():
    for i in range(32):
        val = str(format(i,'05b'))
        exec("register_dict.update({'R{}': '{}'})".format(str(i),val))
#encoding types of all 17 instructions (we will go with A, B, C and D), 4 types given in the doc
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

#we will go through the code in one iteration and see where the labels are then assign them with their line number 
label_dict = {

}
def main():
    pass
    #print(register_dict)

if __name__ == "__main__":
    main()