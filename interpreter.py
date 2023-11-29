"""
 ██████╗  ██████╗   █████╗  ██╗ ███╗   ██╗ ███████╗ ██╗   ██╗  ██████╗ ██╗  ██╗
 ██╔══██╗ ██╔══██╗ ██╔══██╗ ██║ ████╗  ██║ ██╔════╝ ██║   ██║ ██╔════╝ ██║ ██╔╝
 ██████╔╝ ██████╔╝ ███████║ ██║ ██╔██╗ ██║ █████╗   ██║   ██║ ██║      █████╔╝ 
 ██╔══██╗ ██╔══██╗ ██╔══██║ ██║ ██║╚██╗██║ ██╔══╝   ██║   ██║ ██║      ██╔═██╗ 
 ██████╔╝ ██║  ██║ ██║  ██║ ██║ ██║ ╚████║ ██║      ╚██████╔╝ ╚██████╗ ██║  ██╗
 ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ ╚═╝ ╚═╝  ╚═══╝ ╚═╝       ╚═════╝   ╚═════╝ ╚═╝  ╚═╝ Inc0deus

intr:
    > increment data ptr
    < decrement data ptr
    + increment byte at data ptr
    - decrement byte at data ptr
    . output byte at data ptr
    , asign input byte at data ptr
    [ if byte at data ptr is 0, jump to matching ] else continue
    ] if byte at data ptr is not 0, jump to matching [ else continue

HELLO WORLD ! -> "++++++++++[->+++++++>+++++++>+++++++++>+++>+<<<<<]>++.>-.<++++..+++.>>>++.<---.<<.>>-----.<<---.>-.>>+.>+++."

"""

import time

# ANSSI CODE
C_GRAY       = "\033[90m"
C_RED        = "\033[31m"
C_GREEN      = "\033[32m"
C_YELLOW     = "\033[33m"
C_BLUE       = "\033[34m"
C_MAGENTA    = "\033[35m"
C_CYAN       = "\033[36m"
C_LIGHTGRAY  = "\033[37m"
C_WHITE      = "\033[00m"

LINE_UP      = "\033[1A"
DEL_L_TO_END = "\033[0K"    # delete from cursor to end of the line
DEL_L_ALL    = "\033[2K"    # delete all the line
DEL_ALL      = "\033[2J"    # delete all screen
CURSOR_HOME  = "\033[H"     # set cursor to (0, 0)

brainfuck = "\
 ___   ___     _     ___   _  _   ___       _  _ \n\
| _ ) | _ \   /_\   |_ _| | \| | | __|     | |/ /\n\
| _ \ |   /  / _ \   | |  | .` | | _|  X X | ' < \n\
|___/ |_|_\ /_/ \_\ |___| |_|\_| |_|       |_|\_\\\n"

print(CURSOR_HOME + DEL_ALL, end="")
print(C_CYAN + brainfuck + C_WHITE + "\n")
file_path = input(f"{C_CYAN}FILE PATH: {C_WHITE}")
code = open(file_path, "r").read()

# find loops
loop_stack = []
loop_start = {}
loop_end = {}
for i in range(len(code)):
    if code[i] == "[":
        loop_stack.append(i)
    if code[i] == "]":
        if len(loop_stack) == 0: raise SyntaxError(f"{C_RED} MISSING MATCHING \"[\"")
        j = loop_stack.pop()
        loop_end[j] = i
        loop_start[i] = j
if len(loop_stack) > 0: raise SyntaxError(f"{C_RED} MISSING MATCHING \"]\"")

MAX_LENGTH = 30000
ASCII_IO = False

data = [0]
data_ptr = 0    # data pointer
instr_ptr = 0    # instruction pointer

MAX_CONSOLE_DISPLAY = 20
console = []

while instr_ptr < len(code):
    intr = code[instr_ptr]

    # basic intr
    if intr == ">":
        data_ptr += 1
        if data_ptr > MAX_LENGTH: raise MemoryError(f"{C_RED}DATA POINTER OVER {MAX_LENGTH}{C_WHITE}")
        if data_ptr >= len(data): data.append(0)
    if intr == "<":
        data_ptr -= 1
        if data_ptr < 0: raise MemoryError(f"{C_RED}DATA POINTER UNDER 0{C_WHITE}")
    if intr == "+":
        data[data_ptr] += 1
        if 0 > data[data_ptr] or data[data_ptr] > 255: raise ValueError(f"{C_RED}DATA AT ({data_ptr}) AS A VALUE OUT OF RANGE{C_WHITE}")
    if intr == "-":
        data[data_ptr] -= 1
        if 0 > data[data_ptr] or data[data_ptr] > 255: raise ValueError(f"{C_RED}DATA AT ({data_ptr}) AS A VALUE OUT OF RANGE{C_WHITE}")
    if intr == "[":
        if data[data_ptr] == 0: instr_ptr = loop_end[instr_ptr]
    if intr == "]":
        if data[data_ptr] != 0: instr_ptr = loop_start[instr_ptr]

    if len(console) > MAX_CONSOLE_DISPLAY:
        console = console[len(console)-MAX_CONSOLE_DISPLAY:]

    # show terminal
    for i in range(50): print(DEL_L_ALL + LINE_UP, end="")
    print(C_CYAN + brainfuck + C_WHITE)
    print("[" + " ".join([f"{data[i]:<3}" for i in range(len(data))]), "...]")
    print(f"{C_RED} " + " "*(4*data_ptr) + f"^——{C_WHITE}")
    for i in range(len(console)): print(console[i])

    # IO intr
    if intr == ".":
        out = f"{data[data_ptr]:3} {C_GREEN}{repr(chr(data[data_ptr]))}{C_WHITE}"
        if ASCII_IO: out = repr(chr(data[data_ptr]))
        console.append(f"{C_CYAN}OUTPUT:{C_WHITE} {out}")
    if intr == ",":
        inp = input(f"{C_YELLOW}INPUT :{C_WHITE} ")
        if not inp.isdigit(): data[data_ptr] = ord(inp)
        elif 0 <= int(inp) <= 255: data[data_ptr] = int(inp)
        else: raise ValueError(f"{C_RED}INVALID INPUT{C_WHITE}")
        console.append(f"{C_CYAN}INPUT :{C_WHITE} {inp:>3}")

    instr_ptr += 1
    
    time.sleep(0.05)

# show (final) terminal
for i in range(50): print(DEL_L_ALL + LINE_UP, end="")
print(C_CYAN + brainfuck + C_WHITE)
print("[" + " ".join([f"{data[i]:<3}" for i in range(len(data))]), "...]")
print(f"{C_RED} " + " "*(4*data_ptr) + f"^——{C_WHITE}")
for i in range(len(console)): print(console[i])
print()
