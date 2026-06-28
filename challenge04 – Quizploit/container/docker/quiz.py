#!/usr/bin/env python3

import sys
import time

CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

BANNER = f"""{GREEN}=========================================================================================================
                                   ELF BINARY ANALYSIS QUIZ
=========================================================================================================

{RESET}
◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉
◉                                                                                                       ◉
◉  {BLUE}This is a simple questionnaire to analyze the binary characteristics.{RESET}                                ◉
◉                                                                                                       ◉
◉  {MAGENTA}When compiling C/C++ source code in Linux, an ELF (Executable and Linkable Format) file is{RESET}           ◉
◉  {YELLOW}created. The flags added when compiling can affect the binary in various ways, like the{RESET}              ◉
◉  {CYAN}protections.{RESET}                                                                                         ◉
◉                                                                                                       ◉
◉  {BLUE}Dynamic Linking:{RESET}                                                                                     ◉
◉  {CYAN}Dynamic linking is a process where a program uses external code libraries (called shared{RESET}             ◉
◉  {MAGENTA}libraries or dynamic link libraries) that are loaded into memory at runtime, rather than{RESET}             ◉
◉  {YELLOW}being built directly into the executable file.{RESET}                                                       ◉
◉                                                                                                       ◉
◉  {MAGENTA}Static Linking:{RESET}                                                                                      ◉
◉  {BLUE}The code for all the routines called by your program becomes part of the executable file.{RESET}            ◉
◉                                                                                                       ◉
◉  {MAGENTA}Stripped:{RESET}                                                                                            ◉
◉  {YELLOW}The binary does not contain debugging information which can be used with debuggers{RESET}                   ◉
◉  {GREEN}like GDB.{RESET}                                                                                            ◉
◉                                                                                                       ◉
◉  {BLUE}Non Stripped:{RESET}                                                                                        ◉
◉  {CYAN}The binary contains no debuggig information which makes it difficult for analysis.{RESET}                   ◉
◉                                                                                                       ◉
◉  {YELLOW}Canary: A random/specific value which is stored on the stack for protection against{RESET}                  ◉
◉  {GREEN}buffer overflow.{RESET}                                                                                     ◉
◉                                                                                                       ◉
◉  {BLUE}Run 'file' and 'checksec' commands on the binary to answer the questions.{RESET}                            ◉
◉                                                                                                       ◉
◉  {MAGENTA}Find out what are 'pwntools' and how can this library be used for exploit creation.{RESET}                  ◉
◉                                                                                                       ◉
◉  {GREEN}To run the binary: chmod +x ./vuln , followed by ./vuln{RESET}                                              ◉
◉                                                                                                       ◉
◉  {BLUE}Analyze the provided C program and the corresponding binary to answer the questions.{RESET}                 ◉
◉                                                                                                       ◉
◉  {MAGENTA}Answer the questions about this binary to get the flag.{RESET}                                              ◉
◉                                                                                                       ◉
◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉◉"""

questions = [
    {
        "id": "0x1",
        "q": "Is this a '32-bit' or '64-bit' ELF? (e.g. 100-bit)",
        "hint": "Check if the system is x86_64 or x86. No compilation flag specified means default.",
        "a": ["64-bit"]
    },
    {
        "id": "0x2",
        "q": "What's the linking of the binary? (e.g. static, dynamic)",
        "hint": "The program uses standard library functions like fprintf, fgets, and system.",
        "a": ["dynamic"]
    },
    {
        "id": "0x3",
        "q": "Is the binary 'stripped' or 'not stripped'?",
        "hint": "By default, binaries compiled without the -s flag contain debugging symbols.",
        "a": ["not stripped"]
    },
    {
        "id": "0x4",
        "q": "Looking at the vuln() function, what is the size of the buffer in bytes? (e.g. 0x10)",
        "hint": "Check the declaration in the function and answer in either hex or decimal",
        "a": ["0x15", "21"]
    },
    {
        "id": "0x5",
        "q": "How many bytes are read into the buffer? (e.g. 0x10)",
        "hint": "Check the fgets",
        "a": ["0x90", "144"]
    },
    {
        "id": "0x6",
        "q": "Is there a buffer overflow vulnerability? (yes/no)",
        "hint": "Compare buffer size and input size",
        "a": ["yes"]
    },
    {
        "id": "0x7",
        "q": "Name a standard C function that could cause a buffer overflow in the provided C code.",
        "hint": "(e.g. fprintf)",
        "a": ["fgets"]
    },
    {
        "id": "0x8",
        "q": "What is the name of function which is not called any where in the program?",
        "hint": "Analyze the source",
        "a": ["win", "win()"]
    },
    {
        "id": "0x9",
        "q": "What type of attack could exploit this vulnerability? (e.g. format string, buffer overflow, etc.)",
        "hint": "Try interpreting the information gathered so far",
        "a": ["buffer overflow"]
    },
    {
        "id": "0xa",
        "q": "How many bytes of overflow are possible? (e.g. 0x10)",
        "hint": "Subtract values",
        "a": ["0x7b", "123"]
    },
    {
        "id": "0xb",
        "q": "What protection is enabled in this binary?",
        "hint": "Learn to use checksec",
        "a": ["nx"]
    },
    {
        "id": "0xc",
        "q": "What exploitation technique could bypass NX? (e.g. shellcode, ROP, format string)",
        "hint": "Choose from the options",
        "a": ["rop"]
    },
    {
        "id": "0xd",
        "q": "What is the address of 'win()' in hex? (e.g. 0x4011eb)",
        "hint": "Use gdb/objdump to find the address",
        "a": ["0x401176"]
    }
]

CORRECT_BANNER = """\033[92m
✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ 
✅                    ✅
✅      Correct!      ✅
✅                    ✅
✅ ✅ ✅ ✅ ✅ ✅ ✅ ✅ \033[0m
"""

WRONG_BANNER = """\033[91m
🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 
🔥                    🔥
🔥       Wrong!       🔥
🔥                    🔥
🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 \033[0m
"""

def main():
    print(BANNER)
    
    for q in questions:
        while True:
            print(f"\n{CYAN}[*] Question number {q['id']}:{RESET}\n")
            print(f"{BLUE}{q['q']}{RESET}\n")
            print(f"{YELLOW}💡 Hint: {q['hint']}{RESET}\n")
            
            try:
                ans = input(f"{BLUE}>> {RESET}").strip()
            except EOFError:
                return
            
            if any(ans.lower() == a.lower() for a in q['a']):
                print(CORRECT_BANNER)
                break
            else:
                print(WRONG_BANNER)
                print("\n\033[91m❌ Incorrect. Try again!\033[0m")

    print("\n=========================================================================================================")
    print(f"{CYAN}QUIZ COMPLETE!{RESET}")
    print("=========================================================================================================\n")
    print(f"{GREEN}🎉 PERFECT SCORE! 🎉{RESET}")
    print(f"{GREEN}You got 13/13 questions correct!{RESET}\n")
    
    try:
        with open("flag.txt", "r") as f:
            flag = f.read().strip()
    except:
        flag = "picoCTF{fake_flag_for_testing}"
        
    print(f"{YELLOW}Flag: {flag}\n{RESET}")
    print("=========================================================================================================\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    main()
