# 🔐 CthulhuCrypt 

*"An encryption algorithm so chaotic, it might summon eldritch horrors"*

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT)

A Python package featuring **multi-layered, non-linear encryption** combining:
- Bitwise XOR with golden ratio constants
- Dynamic substitution tables  
- Chaotic math (primes, Collatz conjecture, trig functions)
- Recursive encryption pipelines

# 🌟 Features
**Brute-force resistant:** 10+ transformation layers

**Position-dependent ops:** Identical chars → different outputs

**Zero dependencies:** Pure Python (math only)

**CLI support:** Encrypt text from terminal

# ⚡ Quick Start

`pip install cthulhucrypt`

```python
from cthulhucrypt import ultra_encrypt

encrypted = ultra_encrypt("hello", iterations=7)
print(encrypted)  # Output: Ý°FtÔÖr&¥[8ª...
```

# 🔮 CLI Usage

## See all commands
`cthulhucrypt --help`

## Just run character pairing
`cthulhucrypt character-pairing-cli "hello"`

## Ultra-encrypt a string
`cthulhucrypt ultra-encrypt-cli "hello" --iterations 7`

# 🧠 Algorithm Breakdown

## Character Pairing:
`('h','e') → 104*101 = 10504 → [1,0,5,0,4]`

## Dynamic Substitution:
9 rotating substitution tables selected via `sqrt(ascii_sum)*π + log(len)`

## Bitwise Chaos:
`((char ^ position ^ 1618) << (i%3)) & 0xFF`

## Math Destruction:
Collatz conjecture + prime-modulated trig functions

# 💀 Warning
**Not for passwords:** No salting/key stretching

Not quantum-safe: Elder gods might crack it

Pure chaos: No guaranteed decryption (by design)