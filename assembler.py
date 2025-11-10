import sys
import re

registers = {
    "zero": 0,
    "at": 1,
    "v0": 2,
    "v1": 3,
    "a0": 4,
    "a1": 5,
    "a2": 6,
    "a3": 7,
    "t0": 8,
    "t1": 9,
    "t2": 10,
    "t3": 11,
    "t4": 12,
    "t5": 13,
    "t6": 14,
    "t7": 15,
    "s0": 16,
    "s1": 17,
    "s2": 18,
    "s3": 19,
    "s4": 20,
    "s5": 21,
    "s6": 22,
    "s7": 23,
    "t8": 24,
    "t9": 25,
    "k0": 26,
    "k1": 27,
    "gp": 28,
    "sp": 29,
    "fp": 30,
    "ra": 31
}
r = {
    "add": "100000",
    "sub": "100010",
    "and": "100100",
    "or": "100101",
    "xor": "100110",
    "slt": "101010",
    "sll": "000000",
    "srl": "000010",
    "jr": "001000",
    "nop": "000000"
}
j = {
    "j": "000010",
    "jal": "000011"
}
i = {
    "addi": "001000",
    "slti": "001010",
    "lui": "001111",
    "lw": "100011",
    "sw": "101011",
    "beq": "000100",
    "bne": "000101"
}

def removeComments(line: str) -> str:
    return line.split('#')[0].strip()

def toBinary(value:int, bits:int) -> str:
    mask = (1 << bits) - 1
    return format(value & mask, f"0{bits}b")

def parseRegister(reg: str):
    if not reg.startswith('$'):
        raise ValueError(f"not a register idiot {reg}")
    reg_name = reg[1:]
    if reg_name not in registers:
        raise ValueError(f"not a real register goofy {reg}")
    return registers[reg_name]

def parseOperand(operand: str):
    if operand.startswith('$'):
        return parseRegister(operand)
    else:
        return int(operand)

def translateInst(instruction):
    if instruction.startswith('.') or instruction.endswith(':'):
        return ""
    
    line = removeComments(instruction)
    if not line:
        return ""
    
    if line == "nop":
        return "00000000000000000000000000000000"
    
    tokens = line.replace(',', ' ').replace('(', ' ').replace(')', ' ').split()
    mnemonic = tokens[0].lower()

    #R-Type
    if mnemonic in r:
        funct = r[mnemonic]
        if mnemonic == "jr":
            rs = toBinary(parseRegister(tokens[1]), 5)
            rd = toBinary(0, 5)
            rt = toBinary(0, 5)
            shamt = toBinary(0, 5)
            opcode = "000000"
            binary_inst = f"{opcode}{rs}{rt}{rd}{shamt}{funct}"
            return binary_inst
        elif mnemonic in ["sll", "srl"]:
            rd = toBinary(parseRegister(tokens[1]), 5)
            rt = toBinary(parseRegister(tokens[2]), 5)
            shamt = toBinary(int(tokens[3]) & 0x1F, 5)
            rs = toBinary(0, 5)
            opcode = "000000"
            binary_inst = f"{opcode}{rs}{rt}{rd}{shamt}{funct}"
            return binary_inst
        else:
            rd = toBinary(parseRegister(tokens[1]), 5)
            rs = toBinary(parseRegister(tokens[2]), 5)
            rt = toBinary(parseRegister(tokens[3]), 5)
            shamt = toBinary(0, 5)
            opcode = "000000"
            binary_inst = f"{opcode}{rs}{rt}{rd}{shamt}{funct}"
            return binary_inst
        
    #I-Type
    if mnemonic in i:
        opcode = i[mnemonic]
        if mnemonic == "lui":
            rt = toBinary(parseRegister(tokens[1]), 5)
            immediate = toBinary(int(tokens[2]) & 0xFFFF, 16)
            rs = toBinary(0, 5)
        elif mnemonic in ["lw", "sw"]:
            rt = toBinary(parseRegister(tokens[1]), 5)
            immediate = toBinary(int(tokens[2]) & 0xFFFF, 16)
            rs = toBinary(parseRegister(tokens[3]), 5)
        elif mnemonic in ["beq", "bne"]:
            rs = toBinary(parseRegister(tokens[1]), 5)
            rt = toBinary(parseRegister(tokens[2]), 5)
            immediate = toBinary(int(tokens[3]) & 0xFFFF, 16)
        else:
            rt = toBinary(parseRegister(tokens[1]), 5)
            rs = toBinary(parseRegister(tokens[2]), 5)
            immediate = toBinary(int(tokens[3]) & 0xFFFF, 16)
        binary_inst = f"{opcode}{rs}{rt}{immediate}"
        return binary_inst
    
    #J-Type
    if mnemonic in j:
        opcode = j[mnemonic]
        address = toBinary(int(tokens[1]) & 0x03FFFFFF, 26)
        binary_inst = f"{opcode}{address}"
        return binary_inst
    raise ValueError(f"invalid instruction: {mnemonic}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python assembler.py <input_file> <output_file>")
        sys.exit(1)
    
    input, output = sys.argv[1], sys.argv[2]
    try:
        with open(input, 'r') as inf, open(output, 'w') as outf:
            for line in inf:
                try:
                    result = translateInst(line)
                    if result:
                        outf.write(result + '\n')
                except ValueError as e:
                    outf.write(f"wtf is this: {e}\n")
    except FileNotFoundError as e:
        print(f"file not here dummy: {e}\n")
        sys.exit(1)
    
if __name__ == "__main__":
    main()