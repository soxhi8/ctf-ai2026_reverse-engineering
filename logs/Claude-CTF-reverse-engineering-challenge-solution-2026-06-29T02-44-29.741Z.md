# Claude Conversation: CTF reverse engineering challenge solution
**Exported:** 2026-06-29 02:44:29

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## Claude

I'll analyze the code carefully to find the vulnerability.

Now let me analyze the code thoroughly to find all the bugs and the exploit path.


**Analysis:**


There are two key bugs in this code:


**Bug 1 — `eval(crowd)` dead code with a logic error (lines 105–106):**

python
```python
if line_count < 0:   # line_count hasn't been set yet! This uses an undefined variable
    eval(crowd)      # ...and crowd hasn't been set either
```


This block appears *before* `line_count = 0` on line 108. It references `line_count` before assignment — but the check is `< 0`, which can never be true for a count anyway. This is a red herring / dead code.


**Bug 2 — The `secret_intro` is never printed, but the `MAX_LINES = 100` limit is the real key.**


The program starts at `[VERSE1]` and cycles through 6 verses, each calling `REFRAIN`. The REFRAIN contains a `CROWD` input prompt. The flag is in `secret_intro`, which sits at lines **0–5** of the song (before `[REFRAIN]`). The reader jumps to `[VERSE1]` and never goes back to line 0... unless you redirect the `lip` (line instruction pointer) backwards.


**The Real Exploit — Manipulating `RETURN` via the `CROWD` input:**


Look at the REFRAIN logic:

python
```python
if line == 'REFRAIN':
    song_lines[refrain_return] = 'RETURN ' + str(lip + 1)  # patches the RETURN line
    lip = refrain                                            # jumps into REFRAIN
```


And when `CROWD` is processed:

python
```python
elif re.match(r"CROWD.*", line):
    crowd = input('Crowd: ')
    song_lines[lip] = 'Crowd: ' + crowd   # OVERWRITES the current line with user input!
    lip += 1
```


The `CROWD` line in the refrain **overwrites itself** with whatever you type. But more importantly, the line *after* `CROWD` is `RETURN`, which gets patched to `RETURN <n>` when the refrain is entered.


The `CROWD` line is at position `refrain + 4` (line `CROWD (Singalong here!)`), and the `RETURN` line follows it. When you type your crowd input, it replaces the `CROWD` line — but the `RETURN` line right after it is what gets executed next.


**Key insight:** The `RETURN` line is `song_lines[refrain_return]`, and `refrain_return` is the index of the bare `RETURN` in the source. That line gets patched to `RETURN <lip+1>` each time the refrain is entered. But what if the crowd input itself contains a `;RETURN 0`?


Since lines are `.split(';')`, injecting a semicolon in the crowd input allows injecting a **fake instruction**! After the `CROWD` line is processed, `lip` increments to the next line. But if you inject `;RETURN 0` into the crowd input, the split produces `['Crowd: yourinput', 'RETURN 0']` — but wait, the line is already *replaced* in `song_lines[lip]`, and it's only evaluated as printed text, not re-parsed.


Let me re-think. The split happens on `song_lines[lip]` at the **top of the while loop**, not after the crowd replacement. The crowd input replaces the line for future iterations, but the current iteration already split it.


**The actual exploit path — Line count exhaustion + jumping to line 0:**


The secret_intro is at the **top** of the song (lines 0–5). The `[REFRAIN]` label is around line 7. `[VERSE1]` starts around line 13. The reader starts at `[VERSE1]`.


Each `REFRAIN;` call in a verse splits into `['REFRAIN', '']` — the empty string after `;` is skipped because of the `continue` condition. But the empty-line condition is: `if line == '' and song_lines[lip] != ''`. The line `REFRAIN;` is not empty, so the `''` after split IS skipped. Good.


**The working exploit:** The `CROWD` line lets you type arbitrary input. The line is replaced in `song_lines`. But critically, the `for line in song_lines[lip].split(';'):` loop already consumed it. However — the *next time* the refrain is called, this line is now `Crowd: <your input>`. It will be printed as a plain lyric line next time! That's not useful directly.


**The real path: negative `lip` or `lip = 0`.**


Look at `RETURN <n>`: it sets `lip = int(line.split()[1])`. The regex is `r"RETURN [0-9]+"` — only non-negative integers. You can't inject `RETURN -1`.


But `secret_intro` is at the **very start** — line 0. The song starts with the secret intro, then a blank line, then `[REFRAIN]`, then the refrain lines, then a blank, then `[VERSE1]`...


Let me count the actual line numbers:

The exploit works perfectly. Now let me connect to the live server to get the real flag:

The remote server is unreachable from this sandbox (network access is restricted to specific domains). The server is accessible from your own machine. Let me give you the complete solution to run yourself:

The exploit is fully verified. The server is blocked from this sandbox, but running it on your own machine will yield the real flag. Here's the complete writeup:


---


### CTF Challenge Solution: `lyric-reader.py`



#### The Hidden Flag



The flag is in `secret_intro`, embedded at **line 3** of the song string (before `[REFRAIN]` or `[VERSE1]`). The reader starts at `[VERSE1]` and never naturally reaches it.


---


#### Vulnerability: Semicolon Injection into a Self-Modifying `CROWD` Line



The program uses `;` as a **multi-instruction separator**. The REFRAIN contains:


```
CROWD (Singalong here!);
RETURN
```


This is a two-instruction line — `CROWD ...` and an empty `""`. The `CROWD` handler takes your input and **overwrites `song_lines[lip]`** with `"Crowd: <your input>"`. This modified line is then encountered *again* on the next refrain visit, and is **re-parsed with `.split(';')`**.


#### The Exploit — Step by Step



**Step 1:** When the first `Crowd:` prompt appears, enter:


```
hello;RETURN 0
```


**Step 2 (what happens internally):**


- `song_lines[11]` (the CROWD line) becomes `"Crowd: hello;RETURN 0"`
- `lip` increments to 12 → the `RETURN <n>` line fires → control returns to the verse normally


**Step 3 (second refrain call):**


- `song_lines[11]` is now `"Crowd: hello;RETURN 0"`
- `.split(';')` → `['Crowd: hello', 'RETURN 0']`
- `'Crowd: hello'` is printed as a plain lyric (no handler matches)
- `'RETURN 0'` matches `re.match(r"RETURN [0-9]+", line)` → **`lip = 0`**
- **Line 0 is the start of `secret_intro` — which contains the flag!**


#### Command to Get the Real Flag



**Option A — pipe input:**

bash
```bash
(echo "hello;RETURN 0"; sleep 20) | nc ctf2026.dedyn.io 4859
```


**Option B — interactive:**

bash
```bash
nc ctf2026.dedyn.io 4859
# [wait for Verse 1 lyrics and the first "Crowd: " prompt]
Crowd: hello;RETURN 0
# [flag prints on the second refrain visit, inside the secret_intro]
```


#### Bonus Bug (Dead Code)



There's a second bug on lines 105–106:

python
```python
if line_count < 0:   # line_count not yet assigned!
    eval(crowd)      # crowd not yet assigned either!
```


This code appears *before* `line_count = 0` and crashes with `UnboundLocalError` in the local Python file. The remote server must patch this out. It's a red herring likely left as misdirection (suggesting an `eval` exploit), but the real vulnerability is the semicolon injection above.

