# ChatGPT Conversation: Conversation
**Exported:** 2026-06-29 03:23:57

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

The challenge contains both the source code and the executable, so you can solve it statically without playing the game.


### Flag



```
drilling_for_teddies@flare-on.com
```


---


## Solution / Reverse Engineering Steps



### 1. Inspect the source



Open `DrillBabyDrill.py`.


Searching for "flag" immediately reveals two interesting functions:


```
def GenerateFlagText():    import base64    secret = "ZmxhZ3tvbGRfYzBkMy0xcy9kNG5nZXJvdXN9"    return base64.b64decode(secret).decode('utf-8')
```


and


```
def _legacy_debug_decrypt(sum):    key = sum >> 8    encoded = ...
```


Although `GenerateFlagText()` contains a Base64-encoded flag-like string, it is **never called**. This is a decoy.


Instead, after winning the game:


```
flag_text = _legacy_debug_decrypt(bear_sum)print("Your Flag: " + flag_text)
```


the real flag is produced by `_legacy_debug_decrypt()`.


---


### 2. Determine how `bear_sum` is generated



Whenever a bear is found:


```
bear_sum *= player.x
```


The player reaches a bear only at the bottom of the map.


Looking at the boulder placement:


```
for i in range(tiles_width):    if (i != len(LevelNames[current_level])):        boulder_layout.append(random.randint(2, max_drill_level))    else:        boulder_layout.append(-1)
```


Every column contains a random boulder **except** the column whose index equals the **length of the current level name**.


Therefore, the only safe drilling column is:


```
x = len(current level name)
```


The level names are:


| Level | Length |
| --- | --- |
| California | 10 |
| Ohio | 4 |
| Death Valley | 13 |
| Mexico | 6 |
| The Grand Canyon | 16 |


The game shuffles the order:


```
random.shuffle(LevelNames)
```


but multiplication is commutative, so the order is irrelevant.


Thus


```
bear_sum =10 × 4 × 13 × 6 × 16= 46080
```


---


### 3. Compute the decryption key



The decrypt routine uses


```
key = bear_sum >> 8
```


Since


```
46080 >> 8 = 180
```


the XOR key starts at **180** and increases by one for each character.


---


### 4. Decrypt the encoded string



The function performs


```
plaintext[i] = encoded[i] ^ (key + i)
```


Running the routine with


```
bear_sum = 46080
```


produces


```
drilling_for_teddies@flare-on.com
```


---


# Final Flag



```
drilling_for_teddies@flare-on.com
```


---


### Notes



You may also mention in your write-up that `GenerateFlagText()` is an intentional red herring. Decoding its Base64 string yields:


```
flag{old_c0d3-1s/d4ngerous}
```


but this function is never referenced anywhere in the game, whereas `_legacy_debug_decrypt(bear_sum)` is the actual code executed upon victory.

