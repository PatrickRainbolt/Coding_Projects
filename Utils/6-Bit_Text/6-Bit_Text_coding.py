"""
6-Bit Text Encoding System with Uppercase Support
-------------------------------------------------

This script implements a compact text encoding system using a custom 64-character set,
where each character is stored using only 6 bits (instead of the usual 8 for ASCII).
This is ideal for saving space when you only need a limited and safe set of characters.

Supported Characters (64 total):
--------------------------------
- Lowercase letters:     a-z
- Digits:                0-9
- Common symbols:        - _ . , : + ! ? = /
- Space:                 ' ' (space)
- Shift character:       ^  (used to indicate that the next character is uppercase)

Uppercase Handling:
-------------------
- To save space, uppercase letters are not stored directly.
- Instead, a special marker character (`^`) is used.
  For example: "HELLO" → "^h^e^l^l^o"
- This keeps all characters within the 64-character limit and still preserves full case.

Compression Format:
-------------------
- Input is converted to internal format using ^ for uppercase letters.
- Each character is mapped to a 6-bit index (0-63).
- All 6-bit values are packed into bytes for compact storage.
- Decoding reverses this process and reconstructs the original text.
"""

# Print explanation when the program starts
print(__doc__)
print("\n\n")

import sys
import shutil

# Define your custom 64-character set
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789 -_.,:+!?=^"

# Create lookup tables
char_to_index = {c: i for i, c in enumerate(CHARSET)}
index_to_char = {i: c for i, c in enumerate(CHARSET)}

SHIFT_CHAR = "^"

# Sanitize input: remove characters not in CHARSET, but allow ^ for internal case handling
def sanitize_input(text: str) -> str:
    sanitized_text = []
    for c in text:
        if c.lower() not in CHARSET and c != SHIFT_CHAR:
            raise ValueError(f"Unsupported character: {c}")
        sanitized_text.append(c)
    return ''.join(sanitized_text)

# Convert text with uppercase to internal format using ^ marker.
def to_internal_format(text: str) -> str:
    text = sanitize_input(text)  # Ensure only valid characters are in the input
    result = []
    for c in text:
        if c.isupper():
            result.append(SHIFT_CHAR)
            result.append(c.lower())
        else:
            result.append(c)
    return ''.join(result)

# Convert internal format (with ^ markers) back to text with uppercase.
def from_internal_format(text: str) -> str:
    result = []
    skip = False
    for i, c in enumerate(text):
        if skip:
            skip = False
            continue
        if c == SHIFT_CHAR and i + 1 < len(text):
            result.append(text[i + 1].upper())
            skip = True
        else:
            result.append(c)
    return ''.join(result)

# Encodes text to compact 6-bit format.
def encode_6bit(text: str) -> bytes:
    text = sanitize_input(text)  # Ensure only valid characters are in the input
    bits = ''
    for c in text:
        bits += format(char_to_index[c], '06b')
    
    # Pad to byte boundary
    if len(bits) % 8 != 0:
        bits += '0' * (8 - len(bits) % 8)
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

# Decodes compact 6-bit bytes to text.
def decode_6bit(data: bytes) -> str:
    bits = ''.join(format(b, '08b') for b in data)
    chars = []
    for i in range(0, len(bits), 6):
        chunk = bits[i:i+6]
        if len(chunk) < 6:
            break
        idx = int(chunk, 2)
        if idx < len(CHARSET):
            chars.append(index_to_char[idx])
    return ''.join(chars)

# Running Examples
print("Running Test Routine:")
print(f"-" * shutil.get_terminal_size().columns)

original_text = "Each Bit And Byte Represents A Unique Value In The Digital World."
print(f"        Original: bytes[{len(original_text.encode('utf-8'))}]:  {original_text}")

# Convert the original text into internal format
internal = to_internal_format(original_text)
print(f" Internal format: bytes[{len(internal.encode('utf-8'))}]:  {internal}")

# Encode the internal format to 6-bit
encoded = encode_6bit(internal)
print(f"   Encoded (hex): bytes[{len(encoded)}]:  {encoded.hex()}")

# Decode the encoded data back to internal format
decoded_internal = decode_6bit(encoded)
print(f"Decoded internal: bytes[{len(decoded_internal.encode('utf-8'))}]:  {decoded_internal}")

# Convert the internal format back to the original text
final_text = from_internal_format(decoded_internal)
print(f"    Final output: bytes[{len(final_text.encode('utf-8'))}]:  {final_text}\n")

# Calculate and display percentage of bytes saved
original_size = len(original_text.encode('utf-8'))
final_size = len(encoded)

# Calculate percentage saved
percentage_saved = abs((original_size - final_size) / original_size) * 100

print(f"Percentage of bytes saved: {percentage_saved:.2f}%\n")


