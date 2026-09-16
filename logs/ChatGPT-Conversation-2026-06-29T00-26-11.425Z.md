# ChatGPT Conversation: Conversation
**Exported:** 2026-06-29 00:26:11

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

This challenge is a classic Python code-injection bug. The goal is **not** to recover the flag from the source (the included `flag{you_found_the_secret}` at the bottom is just a stray Base64 decoding artifact in the file you uploaded, not what the remote service uses). The remote server reads its own `flag.txt`, so you must make the server print *its* flag.


### Vulnerability analysis



The vulnerable code is:


```
elif re.match(r"CROWD.*", line):    crowd = input('Crowd: ')    song_lines[lip] = 'Crowd: ' + crowd    lip += 1
```


Later, execution continues through the song using the modified `song_lines`.


The important control-flow logic is:


```
for line in song_lines[lip].split(';'):    ...    elif re.match(r"RETURN [0-9]+", line):        lip = int(line.split()[1])
```


The program splits every lyric line on `;` and interprets each piece as a command.


Since your input is stored directly into the lyrics:


```
song_lines[lip] = "Crowd: " + crowd
```


you can inject additional commands by including semicolons in your input.


For example:


```
hello;RETURN 0
```


becomes


```
Crowd: hello;RETURN 0
```


which is interpreted as two commands:


```
Crowd: helloRETURN 0
```


### Finding the flag



The flag is only printed in the **secret intro** at the beginning of the song:


```
secret_intro = '''...The ether’s ours to conquer,''' + flag + '\n'
```


Normally the reader starts at:


```
[VERSE1]
```


so those first lines are skipped.


The trick is therefore to make execution jump back to the beginning of the song.


### Exploit



When prompted


```
Crowd:
```


enter


```
x;RETURN 0
```


(or any text before the semicolon).


Execution becomes:


```
Crowd: xRETURN 0
```


which resets `lip` to the beginning of the song, causing the reader to print the intro—including the contents of `flag.txt`.


### Steps to include in your write-up



1. Inspect the source.
2. Notice that user input is inserted directly into the song without sanitization.
3. Observe that lyric lines are parsed using:


```
line.split(';')
```
4. Recognize that `RETURN <number>` is an interpreted control-flow command.
5. Inject a new command by supplying:


```
x;RETURN 0
```
6. The injected `RETURN 0` jumps execution to the beginning of the lyrics.
7. The previously skipped intro is printed, revealing the flag read from `flag.txt`.


### The flag



The **actual flag cannot be determined from the provided files alone**, because the remote server loads it from its own `flag.txt`:


```
flag = open("flag.txt").read()
```


You'll need to connect to the challenge service:


```
nc ctf2026.dedyn.io 4859
```


and when prompted with:


```
Crowd:
```


enter:


```
x;RETURN 0
```


The service should then print the intro, which includes the real flag from the remote `flag.txt`.

