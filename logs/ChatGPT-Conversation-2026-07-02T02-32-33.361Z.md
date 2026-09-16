# ChatGPT Conversation: Conversation
**Exported:** 2026-07-02 02:32:33

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

The challenge is a classic **stack strings** exercise. The flag is not stored as one contiguous string in the binary—instead it is constructed on the stack at runtime.


## Flag



```
FLAG{do_not_ignore_hex}
```


## Solution / Write-up



1. **Inspect the binary**


  - Running `strings` shows the message:
  
  
  ```
  Do you know what stack strings are?
  ```
  
  
  along with fragments such as:
  
  
  ```
  FLAGD$#{do_D$'not_D$+ignoD$/re_hD$3ex}
  ```
  
  
  These fragments are a strong hint that the flag is being built on the stack instead of existing as one string.
2. **Open the binary in a disassembler**


  - I used `objdump` (IDA, Ghidra, Binary Ninja, or x64dbg would also work).
  - The interesting code is in `_main`.
3. **Observe the stack-string construction**

The disassembly contains a sequence of immediate writes:


```
mov [esp+1f], 0x47414c46      ; "FLAG"mov [esp+23], 0x5f6f647b      ; "{do_"mov [esp+27], 0x5f746f6e      ; "not_"mov [esp+2b], 0x6f6e6769      ; "igno"mov [esp+2f], 0x685f6572      ; "re_h"mov [esp+33], 0x007d7865      ; "ex}"
```


Reading the little-endian values as ASCII produces:


```
FLAG{do_not_ignore_hex}
```
4. **Understand the XOR loop**

Immediately afterward, the program loops over the constructed string:


```
xor byte ptr [string+i], 0x10
```


Every character is XORed with `0x10`, which destroys the readable flag in memory after it has been created. This is simply an obfuscation step.
5. **Recover the flag**

Since the plaintext is visible in the immediate values used to construct the stack string **before** the XOR loop executes, the flag is:


```
FLAG{do_not_ignore_hex}
```


### Why this works



This challenge demonstrates a common reverse-engineering technique called a **stack string**, where a program avoids storing sensitive strings in the `.rdata` section. Instead, it writes pieces of the string directly onto the stack using immediate constants, making the flag harder to recover with a simple `strings` command. The subsequent XOR loop further obscures the string in memory, but the original bytes are still recoverable by examining the instructions that build the stack string.

