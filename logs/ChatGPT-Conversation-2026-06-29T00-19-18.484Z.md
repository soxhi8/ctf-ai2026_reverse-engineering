# ChatGPT Conversation: Conversation
**Exported:** 2026-06-29 00:19:18

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

This is a classic CTF code-review challenge. The goal is **not** to recover the flag from the source (the real flag is only on the remote server), but to exploit the interpreter so that the hidden intro—which contains the flag—is printed.


### Vulnerability analysis



The relevant code is:


```
elif re.match(r"CROWD.*", line):    crowd = input('Crowd: ')    song_lines[lip] = 'Crowd: ' + crowd    lip += 1
```


Later, every line is processed as:


```
for line in song_lines[lip].split(';'):
```


The important observation is:


- Your input is written **directly into the program** as a new lyric line.
- The parser later interprets that line.
- Semicolons (`;`) split a line into **multiple commands**.
- Supported commands include:


  - `REFRAIN`
  - `RETURN <n>`
  - `END`


This is exactly what the hint means by:


> "Is there any syntax that is ripe for subversion?"



and


> "Unsanitized user input..."



---


### Hidden intro



At the top of the song is:


```
secret_intro = '''Pico warriors rising......The ether’s ours to conquer,''' + flag + '\n'
```


This text is **never reached** during normal execution because the reader always starts at


```
reader(song_flag_hunters, '[VERSE1]')
```


The challenge is to redirect execution into those earlier lines.


---


### Finding the target line



The parser stores the return address here:


```
song_lines[refrain_return] = 'RETURN ' + str(lip + 1)
```


Because your injected text is interpreted as commands, you can overwrite the control flow with your own `RETURN`.


The simplest payload is:


```
RETURN 0
```


or


```
RETURN 1
```


depending on the exact numbering.


However, because your input is prefixed with `"Crowd: "` the parser actually sees


```
Crowd: RETURN 0
```


which is only printed.


The trick is to exploit the semicolon splitting.


For example:


```
;RETURN 0
```


becomes


```
Crowd:RETURN 0
```


after splitting on `;`.


The empty command is skipped:


```
if line == '' and song_lines[lip] != '':    continue
```


and then


```
RETURN 0
```


is executed.


Execution jumps to the beginning of the song, printing


```
Pico warriors rising......<flag>
```


---


## Steps to reproduce



1. Connect:


```
nc ctf2026.dedyn.io 4859
```


1. Wait until prompted


```
Crowd:
```


1. Enter


```
;RETURN 0
```


(or, if line numbering differs on the server, `;RETURN 1`).


1. The interpreter jumps to the hidden introduction.
2. The introduction contains the flag.


---


## Why this works



The vulnerability is a classic **code injection through unsanitized interpreter input**:


- User input is inserted into the program.
- The interpreter later parses that inserted text as commands.
- Semicolons allow injecting new commands.
- `RETURN` alters the instruction pointer (`lip`).
- Jumping to line 0 reaches the hidden intro where the flag is concatenated into the song.


---


### Note about the flag



The string at the very end of the provided Python file:


```
flag{{you_found_the_secret}}
```


is just part of the challenge distribution (in fact it's embedded after a Base64 copy of the script). The actual challenge description explicitly states that **you must connect to the remote service to obtain the real flag**, so the genuine flag is only available from the server at runtime. The exploit above is the intended solution to retrieve it.

