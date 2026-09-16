# ChatGPT Conversation: Conversation
**Exported:** 2026-06-28 23:42:56

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

The vulnerability is a classic case of **unsanitized input modifying the program's own control flow**.


### Vulnerability analysis



The program stores the song as a mutable list:


```
song_lines = song.splitlines()
```


When it reaches the audience prompt:


```
crowd = input('Crowd: ')song_lines[lip] = 'Crowd: ' + crowd
```


Later, every line is interpreted by splitting on semicolons:


```
for line in song_lines[lip].split(';'):
```


This means your input is **not treated as plain text**. If you enter semicolons, you create additional commands that will be interpreted the next time that line is executed.


The interpreter recognizes commands like:


```
REFRAINRETURN <number>END
```


The hints specifically point toward this:


- "Unsanitized user input..."
- "syntax that is ripe for subversion"


### Finding the hidden section



The file starts with


```
secret_intro = ...
```


which contains


```
"The ether’s ours to conquer, " + flag
```


However, execution normally starts at


```
reader(song_flag_hunters, '[VERSE1]')
```


so the intro is skipped.


If we can force execution back to **line 0**, the intro (and therefore the flag) will be printed.


### Exploit



When prompted


```
Crowd:
```


enter


```
;RETURN 0
```


or equivalently


```
anything;RETURN 0
```


Here's why it works:


The stored line becomes


```
Crowd: ;RETURN 0
```


On the next visit to the refrain, this is split into


```
Crowd:RETURN 0
```


The interpreter executes


```
lip = 0
```


which jumps to the beginning of the song, causing the hidden intro (containing the flag) to be printed.


### Solving remotely



Connect:


```
nc ctf2026.dedyn.io 4859
```


Wait until you see


```
Crowd:
```


Enter


```
;RETURN 0
```


(or `AAAA;RETURN 0`).


The program will eventually jump to the hidden introduction and print the flag.


---


### Write-up you can submit



1. Inspected `lyric-reader.py`.
2. Observed that user input is written directly into `song_lines`.
3. Noticed each line is later interpreted using `split(';')`, allowing command injection.
4. Identified the interpreter commands (`REFRAIN`, `RETURN`, `END`).
5. Saw that the secret intro containing the flag is placed before `[VERSE1]` and is never reached during normal execution.
6. Injected `;RETURN 0` at the `Crowd:` prompt.
7. On the next execution of that lyric line, the injected `RETURN 0` changed the instruction pointer (`lip`) to the beginning of the song.
8. The hidden intro was printed, revealing the flag.


### The flag



The actual flag is **not present in the provided Python file**—it is read at runtime from:


```
flag = open("flag.txt").read()
```


So I cannot determine its value from the attachments alone. Running the exploit against the remote service as described above will cause the service to print the real flag.

