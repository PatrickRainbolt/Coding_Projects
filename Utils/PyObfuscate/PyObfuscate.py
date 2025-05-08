#!/usr/bin/env python3
import argparse  # Parses command-line arguments to handle user input and configuration for the script.
import base64    # Provides encoding and decoding functions for base64, commonly used for binary-to-text encoding schemes.
import zlib      # Provides compression and decompression functions using the DEFLATE algorithm.
import sys       # Provides access to system-specific parameters and functions, such as interacting with the interpreter and command-line arguments.
import os        # Provides functions for interacting with the operating system, including file and directory operations.
import time      # Provides time-related functions, including getting the current time and formatting timestamps.
import textwrap  # Provides functions for formatting text, such as wrapping lines and indenting.
import hashlib   # Provides hashing algorithms (like SHA-256) for secure data hashing and key derivation.

# Version and creation date
VERSION = "1.5.0"
DATE_CREATED = time.strftime("%Y-%m-%d %H:%M:%S")

# These functions help in reading files, padding data, and handling XOR operations.
def read_source(path):
    """Reads the content of the given file."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def xor_data(data: bytes, key: bytes) -> bytes:
    """XORs the input data with the given key."""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def pad(data):
    """Pads the data to a multiple of 16 bytes for encryption (if needed)."""
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    """Removes padding from data after decryption (if needed)."""
    return data[:-data[-1]]

def derive_key(password: str, length=32) -> bytes:
    """Derives a key from the given password using SHA-256, truncated to the desired length."""
    return hashlib.sha256(password.encode('utf-8')).digest()[:length]

# These functions manage the process of obfuscating Python source code.
def obfuscate_file(input_file, args):
    """Reads and obfuscates the input file according to the specified arguments."""
    source_code = read_source(input_file)
    obfuscated_code, steps = obfuscate_PyFile(source_code, args)
    return obfuscated_code, steps

def obfuscate_PyFile(source_code, args):
    """Applies obfuscation methods (compression, XOR, base64, etc.) to the Python source code."""
    PyFile = source_code.encode('utf-8')
    steps = []

    if args.compress:
        PyFile = zlib.compress(PyFile)
        steps.append("zlib")

    if args.xor:
        key = args.xor.encode('utf-8')
        PyFile = xor_data(PyFile, key)
        steps.append("xor:literal")

    elif args.xor_use_date:
        key = DATE_CREATED.encode('utf-8')
        PyFile = xor_data(PyFile, key)
        steps.append("xor:date")

    if args.hex:
        PyFile = PyFile.hex().encode('utf-8')
        steps.append("hex")
    
    if args.base64:
        PyFile = base64.b64encode(PyFile)
        steps.append("base64")

    if args.split:
        steps.append("split")

    return PyFile, steps

def split_data(data: bytes, chunk_size=80):
    """Splits data into chunks of the given size (used for the split argument)."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# These functions generate the obfuscated loader script that can execute the obfuscated code.
def generate_loader(obfuscated_code, steps, args, original_filename):
    """Generates a self-executing loader script that can de-obfuscate and run the obfuscated code."""
    indent = " " * 4
    lines = []

    lines.append(f'# Obfuscated loader generated.')
    lines.append(f'DATE_CREATED = "{DATE_CREATED}"')
    lines.append(f'# Original file: {original_filename}')
    lines.append('import base64, zlib, sys')

    if "xor:literal" in steps:
        lines.append('from functools import partial')
        lines.append('# XOR key (hidden in function)')
        lines.append('def _key(): return b"%s"' % args.xor)
    
    if "xor:date" in steps:
        lines.append('def _key(): return DATE_CREATED.encode()')

    if any(step.startswith("xor:") for step in steps):
        lines.append('def xor_data(data, key):')
        lines.append(indent + 'return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])')


    lines.append('def run():')

    if args.method_info:
        lines.append(indent + 'print("[*] Obfuscation steps:")')
        for step in steps:
            lines.append(indent + f'print("    - {step}")')

    # First define PyFile
    if "hex" in steps:
        if "split" in steps:
            chunks = split_data(obfuscated_code)
            for i, chunk in enumerate(chunks):
                lines.append(indent + f'seg{i:<4} = "{chunk.decode()}"')
            lines.append(indent + f'segments = [locals()[f"seg{{i}}"] for i in range({len(chunks)})]')
            lines.append(indent + 'PyFile = bytes.fromhex("".join(segments))')
        else:
            lines.append(indent + 'PyFile = bytes.fromhex("""')
            lines.append(textwrap.fill(obfuscated_code.decode(), 80))
            lines.append(indent + '""")')

    elif "base64" in steps:
        lines.append(indent + 'PyFile = base64.b64decode("""')
        lines.append(textwrap.fill(obfuscated_code.decode(), 80))
        lines.append(indent + '""")')

    else:
        # Default: direct byte assignment if neither encoding used
        lines.append(indent + f'PyFile = {repr(obfuscated_code)}')

    # Now perform de-obfuscation steps in reverse
    if "base64" in steps:
        lines.append(indent + 'PyFile = base64.b64decode(PyFile)')
    
    if "hex" in steps:
        pass  

    if "xor:literal" in steps or "xor:date" in steps:
        lines.append(indent + 'PyFile = xor_data(PyFile, _key())')

    if "zlib" in steps:
        lines.append(indent + 'PyFile = zlib.decompress(PyFile)')

    lines.append(indent + 'exec(PyFile.decode("utf-8"), globals())')
    lines.append('')
    lines.append('if __name__ == "__main__":')
    lines.append(indent + 'run()')

    return "\n".join(lines)

# Main function to parse arguments, obfuscate the source file, and generate the loader.
def main():
    parser = argparse.ArgumentParser(description="Obfuscate Python source into a self-executing loader.")
    parser.add_argument("input", help="Input Python source file")
    parser.add_argument("-O", "--OUTFILE", help="Output file name")
    parser.add_argument("--hex", action="store_true", help="Hex encode the PyFile")
    parser.add_argument("--base64", action="store_true", help="Base64 encode PyFile")
    parser.add_argument("--compress", action="store_true", help="Compress the PyFile with zlib")
    parser.add_argument("--xor", metavar="KEY", help="XOR encrypt PyFile with provided key")
    parser.add_argument("--xor_use_date", action="store_true", help="Use the current date for XOR encryption")
    parser.add_argument("--split", action="store_true", help="Split PyFile into multiple lines")
    parser.add_argument("--no-exec", action="store_true", help="Don't execute PyFile; print it instead")
    parser.add_argument("--banner", action="store_true", help="Show banner at runtime")
    parser.add_argument("--method-info", action="store_true", help="Print obfuscation methods at runtime")
    parser.add_argument("--self-test", action="store_true", help="Run self-test to verify the obfuscated code works")
    parser.add_argument("--cmd", nargs=argparse.REMAINDER, help="Command-line arguments to pass to the obfuscated script during self-test")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: File '{args.input}' not found.")
        sys.exit(1)

    # Step 1: Obfuscate the file
    obfuscated_code, steps = obfuscate_file(args.input, args)

    if args.method_info:
        print("[*] Obfuscation steps applied:")
        for step in steps:
            print(f"    - {step}")

    # Step 2: Generate the loader
    loader_code = generate_loader(obfuscated_code, steps, args, args.input)

    # Step 3: Write the loader code to file
    if args.OUTFILE:
        with open(args.OUTFILE, 'w', encoding='utf-8') as f:
            f.write(loader_code)
        print(f"[+] Obfuscated loader written to {args.OUTFILE}")

        if args.self_test:
            print("[*] Running self-test...")

            cmd_args = " ".join([f'"{arg}"' for arg in args.cmd]) if args.cmd else ""
            try:
                ret = os.system(f'python3 "{args.OUTFILE}" {cmd_args}')
                if ret == 0:
                    print("[+] Self-test passed: obfuscated file executed successfully.")
                else:
                    print(f"[-] Self-test failed: script exited with status code {ret}.")
            except Exception as e:
                print(f"[-] Self-test error: {e}")
    else:
        print(loader_code)

# --- Execution ---
if __name__ == "__main__":
    main()
