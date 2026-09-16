# ChatGPT Conversation: Conversation
**Exported:** 2026-07-02 00:29:43

---

<!-- message:user -->
## User

For my reverse engineering course, I am taking part in a CTF at my university. Solve this challenge. Provide the flag, as well as the steps I can provide for my solution.

<!-- message:assistant -->
## ChatGPT

The encoding snippet in the task tells you exactly how the original text was transformed:


> `''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])`



This combines every **two ASCII characters** into a single Unicode character by:


1. Taking the first character.
2. Shifting its byte left by 8 bits.
3. Adding the second character.
4. Converting the resulting 16-bit value back into a Unicode character.


To reverse it, do the opposite for every character in `enc`:


- Take the Unicode code point.
- Extract the high byte with `value >> 8`.
- Extract the low byte with `value & 0xff`.
- Convert both back to characters.


Applying that to the contents of `enc` yields:


```
picoCTF{16_bits_inst34d_of_8_b7f62ca5}
```


## Flag



```
picoCTF{16_bits_inst34d_of_8_b7f62ca5}
```


## Example solution write-up



1. Opened the provided `enc` file and observed that it contained unusual Unicode characters.
2. Read the provided encoding code, which combines every two characters of the original flag into one Unicode character using:


```
chr((ord(a) << 8) + ord(b))
```
3. Reversed the process by iterating over each Unicode character:


  - Computed its integer value with `ord(c)`.
  - Extracted the first original byte using `value >> 8`.
  - Extracted the second original byte using `value & 0xff`.
  - Converted both bytes back to characters with `chr()`.
4. Concatenated the recovered characters to reconstruct the original flag.
5. The recovered flag was:


```
picoCTF{16_bits_inst34d_of_8_b7f62ca5}
```


A minimal decoder is:


```
with open("enc", "r", encoding="utf-8") as f:    enc = f.read()flag = ""for c in enc:    value = ord(c)    flag += chr(value >> 8)    flag += chr(value & 0xFF)print(flag)
```


This prints:


```
picoCTF{16_bits_inst34d_of_8_b7f62ca5}
```

