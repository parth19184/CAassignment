from typing import Counter, final
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
dict_01100_1 = {
    "add": "00000",
    "sub": "01000"
}

dict_01100_2 = {
    "and":"111",
    "or":"110",
    "xor":"100",
    "sll":"001"
}
dict_01100_3 = {
    "sra": "101"
}

dict_11000 = {
    "beq": '000',
    "bne": "001",
    "blt": "100",
    "bge": "101"
}
def get_binary_20(num):
    return format(num,'020b')

def get_binary_12(num):
    return format(num,'012b')

def get_offset_00000(word):
    return word.split("(")[0]

def get_r1_00000(word):
    return word.split("(")[1].replace(")","")

def encode_instruction(instruction):
    words_list = instruction.split()
    first_word = words_list[0]
    if type_dict[first_word] == "01100":
        if first_word in dict_01100_1.keys():
            return dict_01100_1[first_word] + "00" + register_dict[words_list[3]] + register_dict[words_list[2]] + "000" + register_dict[words_list[1]] + "0110011"
        elif first_word in dict_01100_2.keys():
            return "00000" + "00" + register_dict[words_list[3]] + register_dict[words_list[2]] + dict_01100_2[first_word] + register_dict[words_list[1]] + "0110011"
        else:
            return "01000" + "00" + register_dict[words_list[3]] + register_dict[words_list[2]] + dict_01100_3[first_word] + register_dict[words_list[1]] + "0110011"
    elif type_dict[first_word] == "11000":
        offset = words_list[3]
        offset = label_dict[offset]
        offset = get_binary_12(offset)
        return offset[0] + offset[2:8] + register_dict[words_list[2]] + register_dict[words_list[1]] + dict_11000[first_word] + offset[8:] + offset[1] + "1100011"
    elif type_dict[first_word] == "00100":
        imm = words_list[3]
        return get_binary_12(int(imm)) + register_dict[words_list[2]] + "000" + register_dict[words_list[1]] + "0010011"
    elif type_dict[first_word] == "00000":      #12 bit offset
        offset = get_offset_00000(words_list[2])
        offset = get_binary_12(int(offset))
        r1 = get_r1_00000(words_list[2])
        return offset + register_dict[r1] + "010" + register_dict[words_list[1]] + "0000011"
    elif type_dict[first_word] =="01000":       #12 bit offset
        offset = get_offset_00000(words_list[2])
        offset = get_binary_12(int(offset))
        r1 = get_r1_00000(words_list[2])
        return offset[:7] + register_dict[words_list[1]] + register_dict[r1] + "010" + offset[7:] + "0100011"
    elif type_dict[first_word] == "11011":       #20 bit offset
        offset = words_list[2]
        offset = get_binary_20(int(offset))
        return offset[0] + offset[10:] + offset[9] + offset[1:9] + register_dict[words_list[1]] + "1101111"
    elif type_dict[first_word] == "11001":      #12 bit offset
        offset = words_list[3]
        offset = get_binary_12(int(offset))
        return offset + register_dict[words_list[2]] + "000" + register_dict[words_list[1]] + "1100111"
    elif type_dict[first_word] == "01101":      #32 bit immediate but we only need the upper 20 bits
        imm = words_list[2]
        imm = get_binary_20(int(imm))
        return imm[0:20] + register_dict[words_list[1]] + "0110111"
#we will go through the code in one iteration and see where the labels are then assign them with their line number 
label_dict = {

}
def create_string(list1):
    final_string = ""
    for i in list1:
        final_string += i + " "
    return final_string[:-1]
def write_file(filename, assembly_list):
    textfile = open(filename, "w")
    for element in assembly_list:
        textfile.write(element + "\n")
    textfile.close()
def main():
    lines = []
    with open('assembly2.txt') as f:     #will take the binary and read it
        for line in f:
            if not line.isspace():
                line_added = line.replace("\n", "")
                lines.append(line_added)
    print(lines)

#firsst iteration for getting branches:
    keys = type_dict.keys()
    line_number = 0
    for instr_line in lines:
        first_word = instr_line.split()[0]
        if first_word not in keys:
            label_dict[first_word[:-1]] = line_number
            line_number += 1
        else:
            line_number += 1
    
    #print(label_dict)
    
    #creating a set off variable that checks if the program is going towards an infinite loop
    checker = 0  #will use later
    #running code starts from here
    final_binary_list = []
    total_instruction_length = len(lines)
    program_counter = 0
    while(program_counter < total_instruction_length):
        instruction_line_string = lines[program_counter]
        if program_counter in label_dict.values():
            list1 = instruction_line_string.split()[1:]
            instruction_line_string = create_string(list1)
        final_binary_list.append(encode_instruction(instruction_line_string))
        #print(final_binary_list)
        program_counter += 1
    write_file("new_binary_file2.txt", final_binary_list)
    print(label_dict)
if __name__ == "__main__":
    main()