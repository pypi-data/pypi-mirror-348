# cthulhucrypt/core.py
import math
import random
import time
import string
from typing import List, Dict

TABLES: List[Dict[str, str]] = [
    {'!': 'n', '"': '[', '#': 'E', '$': 'Z', '%': 'b', '&': 'r', "'": 'Q', '(': 'e', ')': 'L', '*': "'", '+': 'w', ',': 'g', '-': 'h', '.': '2', '/': '+', '0': 'X', '1': 'D', '2': '"', '3': 'v', '4': 'f', '5': '}', '6': 'H', '7': 'K', '8': 'F', '9': '@', ':': 'P', ';': 'V', '<': 'c', '=': '#', '>': '&', '?': ':', '@': '3', 'A': 'm', 'B': '?', 'C': '8', 'D': 'B', 'E': 'x', 'F': 'u', 'G': '4', 'H': 'a', 'I': 'S', 'J': 'M', 'K': 'j', 'L': ';', 'M': 't', 'N': 'W', 'O': 'C', 'P': 'I', 'Q': '=', 'R': 'O', 'S': '/', 'T': '~', 'U': 'U', 'V': '^', 'W': 'o', 'X': '<', 'Y': '(', 'Z': 'Y', '[': ')', '\\': 'N', ']': '*', '^': 'k', '_': 'q', '`': 'i', 'a': ']', 'b': 's', 'c': '9', 'd': 'G', 'e': 'p', 'f': '0', 'g': ',', 'h': '_', 'i': 'J', 'j': '5', 'k': '!', 'l': 'T', 'm': '{', 'n': '7', 'o': 'y', 'p': '>', 'q': '6', 'r': '`', 's': '%', 't': '-', 'u': 'A', 'v': '$', 'w': 'l', 'x': '|', 'y': 'R', 'z': 'z', '{': '\\', '|': 'd', '}': '1', '~': '.'},
    {'!': 's', '"': 'Q', '#': '`', '$': 'z', '%': '6', '&': '"', "'": 'R', '(': '.', ')': 'C', '*': '\\', '+': 'F', ',': ')', '-': 'P', '.': 'e', '/': 'S', '0': '4', '1': 'G', '2': 'B', '3': 'h', '4': '$', '5': '&', '6': 'r', '7': 'A', '8': 'N', '9': 'w', ':': '[', ';': '0', '<': 'O', '=': 'D', '>': 'U', '?': 'K', '@': 'y', 'A': '}', 'B': 'f', 'C': 'd', 'D': 't', 'E': 'H', 'F': '3', 'G': '^', 'H': 'k', 'I': 'Z', 'J': 'l', 'K': '+', 'L': 'g', 'M': '=', 'N': 'E', 'O': 'b', 'P': '7', 'Q': 'j', 'R': ']', 'S': '*', 'T': 'n', 'U': 'm', 'V': '!', 'W': 'J', 'X': '~', 'Y': 'u', 'Z': 'p', '[': '8', '\\': 'o', ']': 'q', '^': 'a', '_': '5', '`': 'L', 'a': '-', 'b': '9', 'c': 'W', 'd': 'i', 'e': '?', 'f': '_', 'g': 'v', 'h': 'x', 'i': 'T', 'j': ',', 'k': ';', 'l': '|', 'm': '(', 'n': 'V', 'o': '%', 'p': '>', 'q': '1', 'r': '2', 's': 'X', 't': 'M', 'u': "'", 'v': '#', 'w': '{', 'x': 'c', 'y': 'Y', 'z': '@', '{': ':', '|': '<', '}': '/', '~': 'I'},
    {'!': '1', '"': 'e', '#': 'u', '$': '.', '%': 'Z', '&': 'C', "'": '2', '(': 'r', ')': 'P', '*': 'g', '+': 'I', ',': 'M', '-': 'h', '.': 'K', '/': '%', '0': '|', '1': 'H', '2': ')', '3': 'i', '4': 'c', '5': 'm', '6': 'N', '7': 'd', '8': 'L', '9': '(', ':': 'B', ';': '-', '<': 'f', '=': '8', '>': '=', '?': 'S', '@': '/', 'A': '~', 'B': 'R', 'C': '7', 'D': '{', 'E': 'v', 'F': ':', 'G': 'p', 'H': 'T', 'I': 'n', 'J': '9', 'K': 'Y', 'L': 'k', 'M': ';', 'N': 'Q', 'O': 'w', 'P': '*', 'Q': '\\', 'R': '>', 'S': '6', 'T': '!', 'U': '[', 'V': '+', 'W': 'F', 'X': '"', 'Y': '@', 'Z': 'q', '[': '`', '\\': 's', ']': 'l', '^': 'b', '_': 'a', '`': 'A', 'a': 'j', 'b': 'E', 'c': ']', 'd': 'O', 'e': '5', 'f': 'G', 'g': '&', 'h': '<', 'i': 't', 'j': '3', 'k': 'y', 'l': 'V', 'm': 'z', 'n': 'D', 'o': 'o', 'p': '_', 'q': '0', 'r': "'", 's': '$', 't': 'U', 'u': 'X', 'v': 'x', 'w': '^', 'x': '?', 'y': 'J', 'z': '}', '{': '#', '|': 'W', '}': ',', '~': '4'},
    {'!': 'U', '"': 'M', '#': 'D', '$': 'e', '%': '&', '&': 'B', "'": ']', '(': 'F', ')': 'A', '*': '<', '+': ')', ',': 'W', '-': 'E', '.': 'X', '/': 'd', '0': 'z', '1': 's', '2': '>', '3': '^', '4': 'J', '5': "'", '6': '}', '7': 'V', '8': 'O', '9': 'Z', ':': 't', ';': 'n', '<': '"', '=': '2', '>': '+', '?': '8', '@': '5', 'A': 'l', 'B': '~', 'C': 'p', 'D': '-', 'E': '.', 'F': 'N', 'G': 'h', 'H': '@', 'I': 'L', 'J': 'S', 'K': '0', 'L': ':', 'M': 'G', 'N': ',', 'O': 'C', 'P': 'T', 'Q': 'Y', 'R': '`', 'S': '4', 'T': 'K', 'U': '9', 'V': '7', 'W': 'j', 'X': 'H', 'Y': '$', 'Z': 'm', '[': '%', '\\': '3', ']': '(', '^': 'i', '_': '/', '`': '?', 'a': '{', 'b': 'g', 'c': '!', 'd': 'k', 'e': '|', 'f': '1', 'g': '=', 'h': 'y', 'i': 'o', 'j': 'I', 'k': '6', 'l': 'v', 'm': 'b', 'n': 'w', 'o': 'a', 'p': 'R', 'q': '\\', 'r': 'Q', 's': '*', 't': 'u', 'u': 'c', 'v': '_', 'w': '[', 'x': '#', 'y': 'x', 'z': 'q', '{': ';', '|': 'f', '}': 'r', '~': 'P'},
    {'!': 'z', '"': 'A', '#': '1', '$': "'", '%': '0', '&': 'I', "'": '/', '(': 'G', ')': '|', '*': '3', '+': '4', ',': ';', '-': '#', '.': 'P', '/': 'W', '0': '8', '1': 'u', '2': 'O', '3': 'R', '4': 'v', '5': '%', '6': 'k', '7': '`', '8': '}', '9': 'c', ':': ',', ';': '<', '<': 'w', '=': 'S', '>': 'Y', '?': 'j', '@': 'D', 'A': 'y', 'B': 'F', 'C': '-', 'D': 'V', 'E': '6', 'F': '@', 'G': '&', 'H': 'n', 'I': 'E', 'J': 'g', 'K': 'h', 'L': '~', 'M': '\\', 'N': ']', 'O': '9', 'P': 'Z', 'Q': '+', 'R': 'M', 'S': 'x', 'T': 'N', 'U': 'T', 'V': 'H', 'W': 'J', 'X': '=', 'Y': 'C', 'Z': '{', '[': 'f', '\\': ')', ']': 'B', '^': 'p', '_': '?', '`': '_', 'a': 'Q', 'b': ':', 'c': '5', 'd': '>', 'e': '!', 'f': 'X', 'g': 'K', 'h': 'U', 'i': 'm', 'j': 't', 'k': 'o', 'l': '[', 'm': '2', 'n': '$', 'o': '.', 'p': 'b', 'q': 'q', 'r': 'd', 's': 'e', 't': 's', 'u': '7', 'v': 'r', 'w': 'L', 'x': 'l', 'y': 'a', 'z': '"', '{': '*', '|': '(', '}': '^', '~': 'i'},
    {'!': 'v', '"': 'h', '#': 'M', '$': 'b', '%': '>', '&': '`', "'": 'm', '(': 'Q', ')': 'U', '*': 'H', '+': 'X', ',': '2', '-': '[', '.': '.', '/': 'q', '0': 'A', '1': 'Y', '2': 'c', '3': '#', '4': 'd', '5': '-', '6': 'f', '7': '7', '8': '?', '9': '8', ':': '0', ';': 'u', '<': '3', '=': 'R', '>': 'J', '?': 'i', '@': 'a', 'A': '9', 'B': 'n', 'C': 'W', 'D': '6', 'E': 'P', 'F': 'r', 'G': 'p', 'H': '!', 'I': '\\', 'J': "'", 'K': 'E', 'L': 'V', 'M': '<', 'N': '_', 'O': '@', 'P': 's', 'Q': 'j', 'R': 'D', 'S': '=', 'T': '1', 'U': ',', 'V': ']', 'W': 'N', 'X': '{', 'Y': 'K', 'Z': 'F', '[': '}', '\\': 'x', ']': '"', '^': 'O', '_': 't', '`': '5', 'a': '|', 'b': '%', 'c': 'S', 'd': ';', 'e': '+', 'f': 'I', 'g': '$', 'h': 'B', 'i': 'g', 'j': '/', 'k': 'z', 'l': '4', 'm': '&', 'n': 'l', 'o': 'e', 'p': 'C', 'q': 'T', 'r': 'k', 's': 'y', 't': 'Z', 'u': '^', 'v': '*', 'w': 'G', 'x': 'L', 'y': 'o', 'z': ':', '{': 'w', '|': ')', '}': '(', '~': '~'},
    {'!': 'd', '"': '"', '#': 'R', '$': 'S', '%': 'I', '&': '{', "'": '>', '(': 'O', ')': 'Q', '*': '^', '+': 'm', ',': '}', '-': '.', '.': '/', '/': 'y', '0': '#', '1': 'x', '2': 't', '3': 'c', '4': 'g', '5': '1', '6': ':', '7': ',', '8': '0', '9': 'B', ':': 'T', ';': '4', '<': '%', '=': 'V', '>': '~', '?': 'p', '@': '=', 'A': ']', 'B': 'o', 'C': 'z', 'D': "'", 'E': 'e', 'F': 'G', 'G': 'Y', 'H': '7', 'I': 'Z', 'J': 'L', 'K': '`', 'L': ';', 'M': '!', 'N': 'H', 'O': '*', 'P': ')', 'Q': '(', 'R': 'j', 'S': 'C', 'T': 's', 'U': 'r', 'V': '-', 'W': 'v', 'X': '|', 'Y': 'A', 'Z': '5', '[': '&', '\\': 'q', ']': '@', '^': 'u', '_': 'K', '`': '9', 'a': '?', 'b': '8', 'c': 'D', 'd': 'W', 'e': 'w', 'f': 'i', 'g': 'F', 'h': 'M', 'i': 'f', 'j': 'h', 'k': 'k', 'l': 'P', 'm': '_', 'n': '6', 'o': '<', 'p': 'a', 'q': '[', 'r': '\\', 's': 'E', 't': 'b', 'u': '$', 'v': '3', 'w': 'n', 'x': 'J', 'y': 'U', 'z': '2', '{': 'N', '|': 'X', '}': 'l', '~': '+'},
    {'!': '4', '"': 'y', '#': 'C', '$': 'f', '%': 'N', '&': 'M', "'": 'G', '(': 'L', ')': '_', '*': '@', '+': 'A', ',': '/', '-': "'", '.': 'i', '/': '<', '0': '"', '1': '-', '2': '#', '3': 'z', '4': '{', '5': 'P', '6': '!', '7': 'b', '8': 'W', '9': 'Y', ':': 'w', ';': '*', '<': 'g', '=': 'X', '>': '%', '?': 'V', '@': '>', 'A': 'I', 'B': 'u', 'C': 'S', 'D': '}', 'E': 'O', 'F': '7', 'G': 'Q', 'H': '(', 'I': '8', 'J': 'H', 'K': 'x', 'L': ';', 'M': ',', 'N': '=', 'O': 's', 'P': '.', 'Q': '&', 'R': '\\', 'S': 'a', 'T': 'd', 'U': 'E', 'V': '$', 'W': 'j', 'X': '5', 'Y': ']', 'Z': '[', '[': '6', '\\': 'm', ']': 'k', '^': '|', '_': 'p', '`': '1', 'a': '3', 'b': '`', 'c': 'c', 'd': 'q', 'e': '2', 'f': 'U', 'g': '9', 'h': ':', 'i': '^', 'j': 'K', 'k': '~', 'l': 'Z', 'm': ')', 'n': 'J', 'o': 'r', 'p': 'n', 'q': 'h', 'r': 'T', 's': 'e', 't': '?', 'u': 'o', 'v': 'F', 'w': 'B', 'x': 'v', 'y': 'l', 'z': 'D', '{': 't', '|': '+', '}': '0', '~': 'R'},
    {'!': ':', '"': 'J', '#': 'v', '$': 'm', '%': 'e', '&': 'g', "'": '|', '(': 'h', ')': 'z', '*': '{', '+': 'a', ',': '!', '-': '-', '.': 'H', '/': 'u', '0': '<', '1': '6', '2': '0', '3': 'B', '4': '`', '5': 'N', '6': '5', '7': '*', '8': 'Y', '9': 'D', ':': 'F', ';': '7', '<': 'r', '=': '}', '>': 'A', '?': 'M', '@': '>', 'A': 'd', 'B': '2', 'C': '$', 'D': '~', 'E': 'U', 'F': '_', 'G': 'C', 'H': 's', 'I': 'V', 'J': '(', 'K': 'q', 'L': 'x', 'M': 'o', 'N': 'Q', 'O': '[', 'P': 'f', 'Q': 'T', 'R': '%', 'S': '\\', 'T': '"', 'U': 'y', 'V': 'S', 'W': "'", 'X': '+', 'Y': '=', 'Z': 'j', '[': '4', '\\': 'E', ']': 'w', '^': 'Z', '_': '&', '`': ',', 'a': 'b', 'b': 'n', 'c': '?', 'd': '.', 'e': 't', 'f': 'K', 'g': 'O', 'h': '@', 'i': '1', 'j': 'p', 'k': '#', 'l': '3', 'm': '/', 'n': 'i', 'o': 'W', 'p': 'G', 'q': '9', 'r': '^', 's': 'l', 't': ';', 'u': 'L', 'v': ']', 'w': 'P', 'x': ')', 'y': 'c', 'z': 'X', '{': 'R', '|': 'I', '}': 'k', '~': '8'},
]

# ==================== REVERSIBLE ENCRYPTION/DECRYPTION FUNCTIONS ====================
def rev_substitute(text, table_idx, reverse=False):
    table = TABLES[table_idx % len(TABLES)]
    if reverse:
        table = {v: k for k, v in table.items()}
    return ''.join(table.get(c, c) for c in text)

def rev_xor_shift(text, key=0x55AA, reverse=False):
    key_bytes = key.to_bytes(2, 'big')
    if not reverse:
        # XOR but keep as characters
        out = []
        for i, c in enumerate(text):
            val = ord(c) ^ key_bytes[i % 2]
            out.append(chr(val))
        return ''.join(out)
    else:
        # Input is characters, XOR directly
        chars = []
        for i, c in enumerate(text):
            val = ord(c) ^ key_bytes[i % 2]
            chars.append(chr(val))
        return ''.join(chars)

def rev_position_transform(text, reverse=False):
    if reverse:
        # Undo the transformation: swap back every two characters
        chars = list(text)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i+1] = chars[i+1], chars[i]
        return ''.join(chars)
    else:
        # Swap every two characters
        chars = list(text)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i+1] = chars[i+1], chars[i]
        return ''.join(chars)

def encrypt(text, debug=False):
    import random
    table_idx = random.randint(0, 7)
    if debug:
        print(f"[DEBUG] Original: {text}")
    step1 = rev_substitute(text, table_idx)
    if debug:
        print(f"[DEBUG] After substitute (table {table_idx}): {step1}")
    step2 = rev_xor_shift(step1)
    if debug:
        print(f"[DEBUG] After xor shift: {step2}")
    step3 = rev_position_transform(step2)
    if debug:
        print(f"[DEBUG] After position transform: {step3}")
    # Convert to hex at the end
    final = ''.join(f"{ord(c):02x}" for c in step3)
    if debug:
        print(f"[DEBUG] Final hex output: {final}")
    return final, table_idx

def decrypt(text, table_idx, debug=False):
    try:
        if debug:
            print(f"[DEBUG] Encrypted input: {text}")
        # Convert hex input to characters
        chars = []
        for i in range(0, len(text), 2):
            byte = int(text[i:i+2], 16)
            chars.append(chr(byte))
        text = ''.join(chars)
        if debug:
            print(f"[DEBUG] After hex conversion: {text}")
        step1 = rev_position_transform(text, reverse=True)
        if debug:
            print(f"[DEBUG] After reverse position transform: {step1}")
        step2 = rev_xor_shift(step1, reverse=True)
        if debug:
            print(f"[DEBUG] After reverse xor shift: {step2}")
        step3 = rev_substitute(step2, table_idx, reverse=True)
        if debug:
            print(f"[DEBUG] After reverse substitute (table {table_idx}): {step3}")
        return step3
    except ValueError:
        raise ValueError("Input must be a valid hex string")

# Avalanche effect

def avalanche_mix(text, seed=0):
    # Use a simple rolling state and cross-character mixing
    state = seed
    result = []
    for i, c in enumerate(text):
        # Mix state, position, and character
        state = (state * 31 + ord(c) * (i + 1)) & 0xFFFFFFFF
        mixed = ord(c) ^ (state & 0xFF) ^ ((state >> 8) & 0xFF)
        result.append(chr((mixed + (state % 251)) % 256))
    return ''.join(result)

# Bitwise xor transformation

def bitwise_xor_transform(text):
    result = []
    for i, char in enumerate(text):
        # XOR with position and golden ratio
        xor_val = ord(char) ^ i ^ int((1 + math.sqrt(5)) * 1000)
        # Bit rotation based on position
        rotated = ((xor_val << (i % 3)) | (xor_val >> (8 - (i % 3)))) & 0xFF
        result.append(chr(rotated))
    return ''.join(result)

# Math chaos

def math_chaos(text):
    result = []
    for i, char in enumerate(text):
        val = ord(char)
        # Sin/Cos/Tan combo with position
        chaos = int(math.sin(val * i) * 1000) ^ (val << (i % 4))
        # Prime number modulation
        prime_mod = chaos * (i+2) if (i+2) in [2,3,5,7,11,13] else chaos
        # Collatz conjecture step
        if prime_mod % 2 == 0:
            prime_mod = prime_mod // 2
        else:
            prime_mod = (3 * prime_mod + 1) % 256
        result.append(chr(prime_mod % 256))
    return ''.join(result)

# Dynamic substitute

def dynamic_substitute(text, tables):
    if len(text) < 1:
        return text
    ascii_sum = sum(ord(c) for c in text[:3])
    # Enhanced table selection with more math
    table_idx = (math.floor(math.sqrt(ascii_sum) * math.pi) + int(math.log(len(text) + 1))) % len(tables)
    return ''.join([tables[table_idx].get(c, c) for c in text])

def shift_unicode_by_prev(text):
    if not text:
        return ""
    result = [text[0]]  # First character stays the same
    for i in range(1, len(text)):
        prev_unicode = ord(text[i-1])
        prev_unicode_str = str(prev_unicode)
        # Take the first two digits (or less if unicode is < 10 or < 100)
        shift_amount = sum(int(d) for d in prev_unicode_str[:2])
        shifted_char = chr(ord(text[i]) + shift_amount)
        result.append(shifted_char)
    return ''.join(result)

def remove_spaces(text):
    result = ""
    for char in text:
        if char != " ":
            result += char
    return result

def character_pairing(text):
    result = []
    # Process in steps of 2
    for i in range(0, len(text) - 1, 2):
        a, b = text[i], text[i+1]
        prod = ord(a) * ord(b)
        # Split product into digits and add as ints
        digits = [int(d) for d in str(prod)]
        result.extend(digits)
    return result

#
# Encryption sets
# 

def std_hash(text):
    s1 = shift_unicode_by_prev(text)
    s2 = dynamic_substitute(s1, TABLES)
    s3 = bitwise_xor_transform(s2)
    s4 = math_chaos(s3)
    s5 = bitwise_xor_transform(s4)
    s6 = remove_spaces(s5)[:1024]
    return s6

def med_hash(text):
    # Step 1: Table substitution
    step1 = dynamic_substitute(text, TABLES)
    # Step 2: Bitwise operations with avalanche mix
    step2 = avalanche_mix(step1, seed=sum(ord(x) for x in text))
    # Step 3: Math chaos
    step3 = math_chaos(step2)
    # Step 4: Final substitution with feedback
    step4 = dynamic_substitute(step3, TABLES[::-1])
    # Step 5: Final avalanche mix
    return avalanche_mix(step4, seed=sum(ord(x) for x in step3))

def high_hash(text, iterations):
    current = text
    for i in range(iterations):
        paired = character_pairing(current)                # Step 1: Pair → digits
        digit_str = ''.join(str(d) for d in paired)       # Step 2: Convert to string
        current = med_hash(digit_str)                # Step 3: Re-encrypt
        current = avalanche_mix(current, seed=sum(ord(x) for x in digit_str) + i)
    return current

def hash2(text, iterations):
    current = text
    for i in range(iterations):
        s1 = character_pairing(current)
        s2 = dynamic_substitute(''.join(str(d) for d in s1), TABLES)
        s3 = bitwise_xor_transform(s2)
        s4 = math_chaos(s3)
        s5 = bitwise_xor_transform(s4)
        for _ in range(10):
            s5 = math_chaos(s5)
            s6 = bitwise_xor_transform(s5)
        # Apply avalanche_mix before removing spaces
        s6 = avalanche_mix(s6, seed=sum(ord(x) for x in s2) + i)
        current = remove_spaces(s6)
    return current

def hash2_high(text, iterations, salt='the_meaning_of_life_is_42', pepper='i_love_liking_tomatoz_star_questionable_laugh_here_star'):
    current = salt+text+pepper
    for i in range(iterations):
        # Mix previous output into next input
        current = med_hash(current + str(i * len(current)))
        current = high_hash(current, iterations)
        current = hash2(current, iterations)
        current = avalanche_mix(current, seed=sum(ord(x) for x in current) + i)
        current = remove_spaces(current)
    return current

def final_message(function, unencrypted, iterations=1, hex_output=False, output_file=None):
    result = None
    try:
        if function == 'med_hash':
            result = remove_spaces(med_hash(unencrypted))
        elif function == 'high_hash':
            result = remove_spaces(high_hash(unencrypted, iterations))
        elif function == 'hash2':
            result = remove_spaces(hash2(unencrypted, iterations))
        elif function == 'hash2_high':
            result = remove_spaces(hash2_high(unencrypted, iterations))
        else:
            raise ValueError(f"Unknown function: {function}")
    except Exception as e:
        raise RuntimeError(f"Error running {function}: {e}")

    output_str = result
    if hex_output:
        # Convert to hex representation
        output_str = result.encode('utf-8').hex()
    if output_file:
        with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
            f.write(str(output_str) + '\n')
        return None
    else:
        return output_str

def collision_test(amount, function_name, str_length=7, iterations=1):
    seen = {}
    results = []
    collision_found = False
    func_map = {
        'med_hash': med_hash,
        'high_hash': lambda s: high_hash(s, iterations or 1),
        'hash2': lambda s: hash2(s, iterations or 1),
        'hash2_high': lambda s: hash2_high(s, iterations or 1),
    }
    encrypt_func = func_map[function_name]
    start_time = time.time()
    collision_line = None
    for _ in range(amount):
        s1 = ''.join(random.choices(string.ascii_letters + string.digits, k=str_length))
        s2 = ''.join(random.choices(string.ascii_letters + string.digits, k=str_length))
        e1 = encrypt_func(s1)
        e2 = encrypt_func(s2)
        if e1 == e2 and s1 != s2:
            collision_line = f"{s1}={e1}, {s2}={e2}, 1"
            results.append(collision_line)
            collision_found = True
            break
        else:
            results.append(f"{s1}={e1}, {s2}={e2}, 0")
    elapsed = time.time() - start_time
    minutes = round(elapsed / 60)
    with open("result.txt", "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")
    if collision_found:
        print("COLLISION:")
        print(collision_line)
        print(f"Collision found! See result.txt. (in {minutes} minutes)")
    else:
        print(f"No collision found in {amount} tests in {minutes} minutes. See result.txt.")