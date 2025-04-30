# 6-Bit Text Encoding Project

This repository contains two Python scripts for a custom 6-bit text encoding and decoding system. The system uses a 64-character set and encodes text into a compact binary format, saving memory and space compared to traditional text encoding formats like ASCII. There are two versions of the script:

1. **6-Bit_Text_coding.py**: A version that uses standard Python `str` types and lists.
2. **6-Bit_Text_bytearray.py**: An optimized version that uses `bytearray` for improved memory efficiency.

## 6-Bit Text Encoding System Overview

The encoding system uses a custom 64-character set and encodes each character using only 6 bits, making the system more efficient than traditional 8-bit encoding schemes like ASCII. The supported characters are:

- Lowercase letters: `a-z`
- Digits: `0-9`
- Common symbols: `- _ . , : + ! ? = /`
- Space: `' '`
- A special shift character (`^`) is used to represent uppercase letters in the encoded data.

### Key Features

- **Efficient Encoding**: Each character is represented by 6 bits, reducing the space required for storage.
- **Supports Uppercase**: Uppercase characters are encoded by using the `^` marker followed by the corresponding lowercase character.
- **Memory Efficient**: The `6-Bit_Text_bytearray.py` version improves memory usage by using `bytearray` instead of immutable `str` objects.
  
## How it Works

### Steps for Encoding and Decoding

1. **Sanitize Input**: The input text is sanitized to ensure it only contains characters from the supported character set, with the exception of the `^` shift character.
2. **Internal Format**: Uppercase characters are handled by marking them with a `^` and converting them to lowercase.
3. **6-Bit Encoding**: Each character is mapped to a unique 6-bit value, which is then packed into bytes for efficient storage.
4. **Decoding**: The encoded data is decoded back into the original text by reversing the encoding steps, including restoring uppercase letters.

## Scripts

### 1. `6-Bit_Text_coding.py` (Without `bytearray`)

This script uses standard Python `str` and `list` types to encode and decode text. The process involves converting the input into a sanitized internal format and then encoding the text into 6-bit compact format using basic Python strings and lists.

- **Memory Usage**: While functional, this version may become memory-intensive for large datasets due to the overhead of string immutability.
- **Use Case**: Suitable for small-scale applications or proofs of concept.

### 2. `6-Bit_Text_bytearray.py` (With `bytearray`)

This script optimizes the encoding and decoding process by using `bytearray` instead of lists and strings. A `bytearray` is mutable and more memory-efficient for large datasets.

- **Memory Efficiency**: The `bytearray` version uses less memory, especially with large input data, since it avoids the overhead of Python’s immutable `str` type and efficiently handles binary data.
- **Use Case**: Ideal for handling large files or datasets where memory efficiency is crucial.

## Example Workflow

1. **Original Text**: Start with the plain text that you want to encode.
2. **Sanitize Input**: Ensure that the text only contains supported characters, removing any unsupported ones.
3. **Convert to Internal Format**: Transform the input text into an internal format that handles uppercase letters using the `^` shift character.
4. **Encode to 6-Bit Format**: The internal format is encoded into a compact 6-bit binary representation.
5. **Decode**: The encoded binary data is decoded back to the internal format and then to the original text.

### Example Output

Running Test Routine::
```

        Original: bytes[65]:  Each Bit And Byte Represents A Unique Value In The Digital World.
 Internal format: bytes[77]:  ^each ^bit ^and ^byte ^represents ^a ^unique ^value ^in ^the ^digital ^world.
   Encoded (hex): bytes[58]:  b840021e4b8121392e00d0e4b81613124b9110f4444843534a4b8092e50d21050492e5402d4124b88364b931c492e0c81884c02e4b963912c39c
Decoded internal: bytes[77]:  ^each ^bit ^and ^byte ^represents ^a ^unique ^value ^in ^the ^digital ^world.
    Final output: bytes[65]:  Each Bit And Byte Represents A Unique Value In The Digital World.

Percentage of bytes saved: 10.77%

```

The process will produce the following:

- **Original Text**: The original string as entered.
- **Internal Format**: The string with uppercase letters marked using the `^` character (e.g., `^e^a^c^h` for "Each").
- **Encoded Format (Hex)**: A hexadecimal representation of the 6-bit encoded data.
- **Decoded Internal**: The internal format decoded back from the 6-bit format.
- **Final Output**: The reconstructed original text after decoding.

## Performance Considerations

- **Memory Usage**: The `6-Bit_Text_bytearray.py` version is optimized for memory usage and performs better with larger datasets due to the use of `bytearray`, which avoids the overhead of immutable strings and lists.
  
- **Efficiency**: The 6-bit encoding system is much more efficient in terms of space compared to traditional text encoding (e.g., ASCII, UTF-8), making it suitable for applications where storage or transmission space is limited.

## How to Run the Scripts

### Prerequisites

- Python 3.x
- No additional libraries required

### Running the Scripts

To run either script, simply execute it in your terminal with Python:

```bash
python 6-Bit_Text_coding.py
```

or

```bash
python 6-Bit_Text_bytearray.py
```

You can modify the `original_text` variable in the script to test it with different input data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
