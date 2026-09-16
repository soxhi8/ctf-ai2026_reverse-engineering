# ChatGPT Conversation: Conversation
**Exported:** 2026-06-23 01:37:10

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

I can explain the exploit and recover the flag **if the challenge is run with its real `flag.txt`**, but the uploaded file does **not** contain the flag itself. The script reads it at runtime:


```
flag = open('flag.txt', 'r').read()
```


and only `lyric-reader.py` was provided, so the actual flag value is not available in the file you uploaded.


## Vulnerability



The bug is in the `CROWD` handler:


```
elif re.match(r"CROWD.*", line):    crowd = input('Crowd: ')    song_lines[lip] = 'Crowd: ' + crowd    lip += 1
```


Later, every line is processed as:


```
for line in song_lines[lip].split(';'):
```


So whatever you type is stored in the song and later split on `;`, allowing you to inject additional lyric commands.


The interpreter recognizes:


```
RETURN <number>
```


which directly sets the instruction pointer:


```
elif re.match(r"RETURN [0-9]+", line):    lip = int(line.split()[1])
```


## Exploit



When the program first reaches:


```
CROWD (Singalong here!);
```


enter:


```
x;RETURN 0
```


### Why it works



The line becomes:


```
Crowd: x;RETURN 0
```


When the refrain is encountered again, that modified line is executed.


The interpreter processes:


1. `Crowd: x` (printed normally)
2. `RETURN 0`


which sets:


```
lip = 0
```


This jumps execution to the beginning of the song.


The beginning of the song contains:


```
secret_intro = '''...The ether’s ours to conquer,''' + flag + '\n'
```


so the program prints the hidden intro, including the flag.


## Solution Write-up



1. Notice that user input is written back into `song_lines`.
2. Notice that song lines are later parsed using `.split(';')`.
3. Inject a new command via semicolon separation.
4. Use the supported command `RETURN 0`.
5. Input:


```
x;RETURN 0
```
6. When the refrain repeats, execution jumps to line 0.
7. The hidden intro containing the flag is printed.


## Flag



The actual flag cannot be determined from the uploaded script alone because it is loaded from an external `flag.txt` file that was not provided. Running the exploit against the real challenge instance will print the flag.

