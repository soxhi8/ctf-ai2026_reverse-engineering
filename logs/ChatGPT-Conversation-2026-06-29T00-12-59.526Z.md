# ChatGPT Conversation: Conversation
**Exported:** 2026-06-29 00:12:59

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

The vulnerability is a classic **script injection through self-modifying control flow**.


### Root cause



The program stores the song as a mutable list:


```
song_lines = song.splitlines()
```


When it reaches the chorus, it does:


```
crowd = input("Crowd: ")song_lines[lip] = "Crowd: " + crowd
```


Later, every line is interpreted as a tiny scripting language:


```
for line in song_lines[lip].split(";"):
```


where tokens like:


- `REFRAIN`
- `RETURN <n>`
- `END`


are treated as control-flow commands.


Because your input is written directly back into the script, anything after a semicolon becomes a new instruction the next time that line is executed.


### Exploit



At the **first** `Crowd:` prompt, enter:


```
A;RETURN 0
```


Here's what happens:


The stored line becomes:


```
Crowd: A;RETURN 0
```


When the refrain is visited again, it is split into:


```
Crowd: ARETURN 0
```


- `Crowd: A` is **not** matched by the regex `CROWD.*` (it's lowercase `Crowd`), so it is simply printed.
- `RETURN 0` is interpreted as a control-flow instruction.
- Execution jumps to line 0, which is the secret intro.


The intro contains:


```
secret_intro = (    ...    + flag + "\n")
```


so the program prints the flag.


---


## Steps for your write-up



1. Inspect `cryptography101.py`.
2. Notice that user input is written back into `song_lines`.
3. Observe that each line is later parsed by splitting on `;`.
4. Realize this allows injection of interpreter commands.
5. Inject:


```
A;RETURN 0
```
6. The interpreter jumps to line 0.
7. The hidden intro (which contains the flag) is printed.


---


## Flag



I can't determine the actual flag from the files you uploaded because `flag.txt` is **not included**—the challenge is designed so the remote server has the real flag.


If you connect to the challenge:


```
nc ctf2026.dedyn.io 4859
```


and, when prompted with:


```
Crowd:
```


enter:


```
A;RETURN 0
```


the service should print the real flag.

