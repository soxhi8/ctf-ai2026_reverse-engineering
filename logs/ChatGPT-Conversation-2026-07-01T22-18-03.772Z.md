# ChatGPT Conversation: Conversation
**Exported:** 2026-07-01 22:18:03

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

This challenge is a classic **interpreter/control-flow injection** bug. The goal is not to reverse a binary, but to understand how the custom "lyrics interpreter" works and abuse it to execute the hidden `PRINT_FLAG` instruction.


### Vulnerability analysis



The interesting part is this code:


```
elif re.match(r"CROWD.*", line):    crowd = input('Crowd: ')    song_lines[lip] = 'Crowd: ' + crowd    lip += 1
```


When the interpreter reaches the `CROWD` line, it:


1. Reads your input.
2. **Replaces the current line** with:


```
Crowd: <your input>
```


Later, execution can jump back to this line.


The interpreter processes each line by splitting on semicolons:


```
for line in song_lines[lip].split(';'):
```


It also recognizes special commands:


- `REFRAIN`
- `RETURN n`
- `PRINT_FLAG`
- `END`


So if your input contains semicolons, you can inject additional interpreter commands.


---


### How the control flow works



When `REFRAIN` is encountered:


```
song_lines[refrain_return] = 'RETURN ' + str(lip + 1)lip = refrain
```


The `RETURN` line is rewritten so that execution returns to the line after the `REFRAIN` call.


Inside the refrain there is:


```
CROWD (Singalong here!);RETURN
```


Normally this becomes something like:


```
Crowd: helloRETURN 17
```


and execution continues normally.


However, since your input is inserted verbatim, you can make that line become:


```
Crowd: anything;PRINT_FLAG
```


When execution later reaches that modified line again, it is split into


```
Crowd: anythingPRINT_FLAG
```


The interpreter prints the first part as ordinary text, then executes the hidden instruction:


```
elif line == 'PRINT_FLAG':    print(flag)
```


---


## Exploit



When prompted:


```
Crowd:
```


enter


```
test;PRINT_FLAG
```


(or any text before the semicolon).


The interpreter will execute:


```
Crowd: testPRINT_FLAG
```


and print the contents of `flag.txt`.


---


## Getting the flag



Run the remote service:


```
nc ctf2026.dedyn.io 4859
```


When it asks


```
Crowd:
```


type


```
test;PRINT_FLAG
```


The server should then print the flag from its `flag.txt`.


---


## Write-up / Solution steps



1. Read `challenge01.py`.
2. Identify that the interpreter splits every line using `;`.
3. Notice that user input is written directly into the program:


```
song_lines[lip] = "Crowd: " + crowd
```
4. Since the line is later interpreted again, semicolons allow injection of new interpreter commands.
5. The hidden interpreter command is:


```
PRINT_FLAG
```
6. Connect to the challenge server:


```
nc ctf2026.dedyn.io 4859
```
7. When prompted for **Crowd**, enter:


```
test;PRINT_FLAG
```
8. The interpreter executes the injected `PRINT_FLAG` command and prints the flag.


### Flag



The actual flag **cannot be determined from the provided files alone**, because `flag.txt` is **not included**—it exists only on the remote server. Executing the exploit against the provided `nc` service will reveal the flag.

<!-- message:user -->
## User

;PRINT_FLAG
 
Echoes in memory, packets in trace, 
Digging through the remnants to uncover with haste. 
Hex and headers, carving out clues, 
Resurrect the hidden, it's forensics we choose. 
Disk dumps and packet dumps, follow the trail, 
Buried deep in the noise, but we will prevail. 
 
We’re flag hunters in the ether, lighting up the grid, 
No puzzle too dark, no challenge too hid. 
With every exploit we trigger, every byte we decrypt, 
We’re chasing that victory, and we’ll never quit. 
Crowd:  
flag{th1s_1s_n0t_th3-fl4g}

<!-- message:assistant -->
## ChatGPT

That's actually a useful clue.


The program is executing your injected `PRINT_FLAG`, because it printed:


```
flag{th1s_1s_n0t_th3-fl4g}
```


The challenge author intentionally made the local `PRINT_FLAG` output a **decoy flag**. The real flag is almost certainly obtained by exploiting the interpreter further.


Notice the challenge description:


> "There's a hidden refrain this program doesn't print by default."



That wording strongly suggests the intended solution is **not simply calling `PRINT_FLAG`**, but making the interpreter execute a hidden part of the lyrics that contains the real flag.


The decoy indicates you've found one hidden command, but not the intended path.


The next thing I'd investigate is whether we can inject additional control-flow commands, for example:


- `REFRAIN`
- `RETURN n`
- `END`


or manipulate the return address to jump somewhere unexpected.


For example, try payloads like:


```
;REFRAIN
```


```
;RETURN 0
```


```
;RETURN 1
```


or


```
;RETURN 999
```


to see how the interpreter behaves.


The most interesting observation is that this code rewrites the `RETURN` line dynamically:


```
song_lines[refrain_return] = "RETURN " + str(lip + 1)
```


If we can somehow alter where that return goes, we may be able to jump into the hidden intro or another section that isn't normally executed.


Could you also tell me:


- **What happens after** `flag{th1s_1s_n0t_th3-fl4g}`? Does the program terminate?
- Is this challenge hosted on **PicoCTF**, or is it just using PicoCTF code as inspiration?


With that information, we can determine whether this is the original challenge (whose intended exploit is known) or a modified university version.

