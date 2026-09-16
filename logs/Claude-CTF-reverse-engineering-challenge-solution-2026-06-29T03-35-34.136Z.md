# Claude Conversation: CTF reverse engineering challenge solution
**Exported:** 2026-06-29 03:35:34

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## Claude

I'll analyze the code to find the flag. Let me trace through the logic carefully.

The flag is: **`flag{old_c0d3-1s/d4ngerous}`**


(The `TileSway` output `drilling_for_teddies@flare-on.com` is the Flare-On contact email appended after, not part of the flag itself.)


---


### Solution Walkthrough



#### 1. Understanding the win condition



The game has 5 levels. Each level, you must drill to the maximum depth (`max_drill_level = tiles_height - overhead_height = 12`) at a specific X position to find a bear. When all 5 bears are found, `GenerateFlagText(bear_sum)` and `TileSway(bear_sum)` are called and their results are printed.


#### 2. Finding where the bear spawns (the safe column)



In `boulder_layout` generation:

python
```python
if (i != len(LevelNames[current_level])):
    boulder_layout.append(random.randint(2, max_drill_level))
else:
    boulder_layout.append(-1)  # -1 = no boulder = safe to drill to bottom
```


The boulder-free column (where the bear hides) is always at **x = len(level_name)**. All other columns have a random boulder that ends the game.


#### 3. Calculating `bear_sum`



`bear_sum` starts at `1` and is multiplied by `player.x` each time a bear is found:

python
```python
bear_sum *= player.x  # player.x == len(level_name) at that moment
```


The levels are shuffled, but since it's a product, order doesn't matter:


```
10 × 4 × 12 × 6 × 16 = 46080
```


#### 4. Decoding the flag



**`GenerateFlagText`** simply base64-decodes a hardcoded string:

python
```python
base64.b64decode("ZmxhZ3tvbGRfYzBkMy0xcy9kNG5nZXJvdXN9") 
# → flag{old_c0d3-1s/d4ngerous}
```


Note: `bear_sum` is always truthy (never 0), so the `if bear_sum:` branch always runs — the flag is **static and doesn't depend on gameplay at all**.


**`TileSway`** is an XOR cipher where `key = bear_sum >> 8 = 46080 >> 8 = 180`, XORing each byte of the encoded string with `key + i`. This decodes to the Flare-On email address, not part of the flag.


#### Key insight for your writeup



The flag is entirely hardcoded — you don't need to play the game at all. `GenerateFlagText` always returns the base64-decoded string as long as `bear_sum` is non-zero (which it always is, since it's initialized to `1` and only multiplied). Static analysis alone is sufficient.

<!-- message:user -->
## User

the flag is wrong

<!-- message:assistant -->
## Claude

Let me re-examine more carefully.

The flag is **`drilling_for_teddies@flare-on.com`**.


I made an error in my first answer — I didn't recognize the Flare-On flag format. **Flare-On CTF flags are always email addresses ending in `@flare-on.com`**, not `flag{...}` strings. The base64-decoded string was a red herring/decoy embedded in `GenerateFlagText`, while the real flag is produced by `TileSway`.


---


### Corrected Solution Walkthrough



#### 1. Two outputs, one real flag



The game prints: `flag_text + rumble_amount`


- `flag_text` = `flag{old_c0d3-1s/d4ngerous}` — a **decoy**, just a static base64-decoded string
- `rumble_amount` = result of `TileSway(bear_sum)` — the **real flag**


#### 2. Computing `bear_sum`



Each level's bear spawns at column `x = len(level_name)` (the one column with `boulder_layout[x] == -1`). `bear_sum` accumulates as a running product:


| Level | Name | Length |
| --- | --- | --- |
| 0 | California | 10 |
| 1 | Ohio | 4 |
| 2 | Death Valley | 12 |
| 3 | Mexico | 6 |
| 4 | The Grand Canyon | 16 |


`bear_sum = 10 × 4 × 12 × 6 × 16 = 46080` (order doesn't matter — it's multiplication)


#### 3. Decoding `TileSway`


python
```python
key = 46080 >> 8  # = 180 (0xb4)
# XOR each byte of encoded string with (key + i)
# → "drilling_for_teddies@flare-on.com"
```


**Flag: `drilling_for_teddies@flare-on.com`**

