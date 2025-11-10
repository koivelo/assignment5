import sys
import re

registers = {
    "00000": "$zero",
    "00001": "$at",
    "00010": "$v0",
    "00011": "$v1",
    "00100": "$a0",
    "00101": "$a1",
    "00110": "$a2",
    "00111": "$a3",
    "01000": "$t0",
    "01001": "$t1",
    "01010": "$t2",
    "01011": "$t3",
    "01100": "$t4",
    "01101": "$t5",
    "01110": "$t6",
    "01111": "$t7",
    "10000": "$s0",
    "10001": "$s1",
    "10010": "$s2",
    "10011": "$s3",
    "10100": "$s4",
    "10101": "$s5",
    "10110": "$s6",
    "10111": "$s7",
    "11000": "$t8",
    "11001": "$t9",
    "11010": "$k0",
    "11011": "$k1",
    "11100": "$gp",
    "11101": "$sp",
    "11110": "$fp",
    "11111": "$ra"
    }

r = {
        "100000": "add",
        "100010": "sub",
        "100100": "and",
        "100101": "or",
        "100110": "xor",
        "101010": "slt",
        "001000": "jr"
    }

i = {
        "001000": "addi",
        "001010": "slti",
        "001111": "lui",
        "100011": "lw",
        "101011": "sw",
        "000100": "beq",
        "000101": "bne"
}

j = {
        "000010": "j",
        "000011": "jal"
        }

def binaryToInt(binString: str) -> int:
    return int(binString, 2)

def sbToInt(binString: str) -> int:
    value = int(binString, 2)
    if len(binString) > 0 and binString[0] == '1':
        value -= (1 << len(binString))
    return value


def disassembleInst(instruction) -> str:
    line = instruction.strip()
    if not line:
        return ""
    
    if line == "#":
        return ""
    opcode = line[0:6]
    rs = line[6:11]
    rt = line[11:16]
    rd = line[16:21]
    shamt = line[21:26]
    funct = line[26:32]
    immediate = line[16:32]
    address = line[6:32]

    #R-Type
    if opcode == "000000":
        if funct == "000000":
            if rd == "00000" and rt == "00000" and shamt == "00000":
                return "nop"
            else:
                shamtBin = binaryToInt(shamt)
                return f"sll {registers[rd]}, {registers[rt]}, {shamtBin}"
        elif funct == "000010":
            shamtBin = binaryToInt(shamt)
            return f"srl {registers[rd]}, {registers[rt]}, {shamtBin}"
        elif funct in r:
            inst = r[funct]
            if inst == "jr":
                return f"jr {registers[rs]}"
            else:
                return f"{inst} {registers[rd]}, {registers[rs]}, {registers[rt]}"
        else:
            raise ValueError(f"invalid R-type funct: {funct}")

    #I-Type
    if opcode in i:
        inst = i[opcode]
        immVal = sbToInt(immediate)

        if inst == "lui":
            return f"{inst} {registers[rt]}, {immVal}"
        elif inst in ["lw", "sw"]:
            return f"{inst} {registers[rt]}, {immVal}({registers[rs]})"
        elif inst in ["beq", "bne"]:
            return f"{inst} {registers[rs]}, {registers[rt]}, {immVal}"
        else:  # addi, slti
            return f"{inst} {registers[rt]}, {registers[rs]}, {immVal}"

    #J-Type
    if opcode in j:
        inst = j[opcode]
        addrVal = binaryToInt(address)
        return f"{inst} {addrVal}"
    raise ValueError(f"invalid instruction: {instruction}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python assembler.py <input_file> <output_file>")
        sys.exit(1)
    
    input, output = sys.argv[1], sys.argv[2]
    try:
        with open(input, 'r') as inf, open(output, 'w') as outf:
            for line in inf:
                try:
                    result = disassembleInst(line)
                    if result:
                        outf.write(result + '\n')
                except ValueError as e:
                    outf.write(f"wtf is this: {e}\n")
    except FileNotFoundError as e:
        print(f"file not here dummy: {e}\n")
        sys.exit(1)
    
if __name__ == "__main__":
    main()