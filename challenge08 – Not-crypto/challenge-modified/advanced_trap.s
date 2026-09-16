[bits 64]

; 1. Ptrace trap
mov eax, 101       ; sys_ptrace
mov edi, 0         ; PTRACE_TRACEME
xor esi, esi       ; 0
xor edx, edx       ; 0
xor r10d, r10d     ; 0
syscall
test eax, eax
js .debugger_detected

; 2. State-Setup Trap (XOR 0x21a0 with 0x42)
; We are at 0x1e15 (approx)
; We need to lea r8, [rel 0x21a0]
; NASM can calculate relative offset if we know where we are.
; But we can just use call/pop to get RIP.
call .get_rip
.get_rip:
pop r8
; r8 is now at .get_rip
; We know .get_rip will be at 0x1e00 + something.
; Let's just hardcode the relative offset using NASM's rel capability if we specify org?
; No, we will just use python to assemble the exact bytes.

.debugger_detected:
; exit(1)
mov eax, 60
mov edi, 1
syscall
