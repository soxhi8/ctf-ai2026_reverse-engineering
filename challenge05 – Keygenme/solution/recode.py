import hashlib

prefix = b"picoCTF{br1ng_y0ur_0wn_k3y_"
suffix = b"}"

prefix_hash = hashlib.md5(prefix).hexdigest()
suffix_hash = hashlib.md5(suffix).hexdigest()

# Determine memory ranges:
# Ranges from 0x__ to 0x00
# local_78 starts at 0x78
    # Looping from local_78 to local_78+0x20 (len dec 32, towards 0x00) -> range is 0x78 to 0x59
# local_58 starts at 0x58
    # Looping from local_58 to local_58+0x20 (len dec 32, towards 0x00) -> range is 0x58 to 0x39

# Determine memory location of individual variables
# p.e. local_43 refers to the memory offset of the variable, so local_43 -> 0x43 offset
    # 0x43 is in the range of local_58, which is suffix, so part of suffix hash string
    # To find dec position within hash string, deduct 0x43 from 0x58 base -> 88 - 67 = 21

dynamic_part = (
    suffix_hash[21] +  # auStack_38[0x1b] = local_43 (0x58 - 0x43 = 21)
    prefix_hash[22] +  # auStack_38[0x1c] = local_62 (0x78 - 0x62 = 22)
    prefix_hash[22] +  # auStack_38[0x1d] = local_62 (0x78 - 0x62 = 22)
    prefix_hash[0]  +  # auStack_38[0x1e] = local_78[0]
    prefix_hash[29] +  # auStack_38[0x1f] = local_5b (0x78 - 0x5b = 29)
    suffix_hash[21] +  # auStack_38[0x20] = local_43 (0x58 - 0x43 = 21)
    prefix_hash[14] +  # auStack_38[0x21] = local_6a (0x78 - 0x6a = 14)
    prefix_hash[24]    # auStack_38[0x22] = local_60 (0x78 - 0x60 = 24)
    # auStack_38[0x23] = local_ba[0]; closing brace, added in final_flag
)

final_flag = prefix.decode() + dynamic_part + suffix.decode()

print(f"Found flag: {final_flag}")