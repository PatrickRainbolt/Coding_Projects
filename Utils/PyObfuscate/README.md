# PyObfuscate: Python Source Code Obfuscator

PyObfuscate.py is a script designed to obfuscate Python source code by applying various techniques such as XOR encryption, compression, base64 encoding, and more. 
The obfuscation process makes it more difficult for someone to reverse-engineer the original Python code. PyObfuscate also generates a self-executing loader that 
can de-obfuscate and run the obfuscated code.

## Features

- **Compression**: Compress the source code using zlib.
- **XOR Encryption**: Encrypt the source code using a custom key or the current date.
- **Base64 Encoding**: Encode the source code in base64.
- **Hex Encoding**: Encode the source code in hexadecimal format.
- **Code Splitting**: Split the obfuscated code into smaller chunks for easier handling.
- **Self-Executing Loader**: Generates a loader script that can de-obfuscate and run the obfuscated code.
- **Method Info**: Prints the applied obfuscation steps at runtime.
- **Self-Test**: Runs a self-test to verify if the obfuscated code executes properly.


### Command-line Arguments

The script can be run directly from the command line. The basic usage is as follows:

```bash
python3 PyObfuscate.py <input_file> [options]
```

Where `<input_file>` is the Python source code file you want to obfuscate.

### Available Options

* `-O`, `--OUTFILE`: Specify the output filename for the obfuscated loader script.
* `--hex`: Hex encode the Python file.
* `--base64`: Base64 encode the Python file.
* `--compress`: Compress the Python file using zlib.
* `--xor <KEY>`: XOR encrypt the Python file with the specified key.
* `--xor_use_date`: XOR encrypt the Python file using the current date as the key.
* `--split`: Split the Python file into multiple chunks.
* `--no-exec`: Do not execute the obfuscated file; print the loader script instead.
* `--banner`: Display a banner at runtime.
* `--method-info`: Print the obfuscation steps applied at runtime.
* `--self-test`: Run a self-test to verify the obfuscated code works.
* `--cmd <args>`: Command-line arguments to pass to the obfuscated script during the self-test.
* `-V`, `--version`: Display the version of the script.

### Example Usage

To obfuscate a Python file and generate a loader script:

```bash
python3 PyObfuscate.py myscript.py -O obfuscated_loader.py --base64 --xor "mysecretkey" --compress
```

This will:

* Base64 encode the Python file.
* XOR encrypt the Python file with the key `"mysecretkey"`.
* Compress the Python file using zlib.
* Generate a self-executing loader script named `obfuscated_loader.py`.

To run a self-test and ensure the obfuscated code works:

```bash
python3 PyObfuscate.py myscript.py --self-test --cmd "arg1" "arg2"
```

### Output

The script generates a loader script that can be executed directly. The loader will:

1. Reverse the obfuscation steps.
2. Decrypt, decompress, or decode the original Python code.
3. Execute the original code.

## Example of a program being converted

CMD: cat PyMathDemo.py
```python
#!/usr/bin/env python3
import math   # The math library provides mathematical functions and constants such as trigonometric, logarithmic, and other advanced mathematical operations.

# Define some math functions with descriptions
def test_functions():
    functions = [
        {"name": "Addition", "equation": "5 + 3", "result": 5 + 3, "description": "Combining two or more numbers to get a sum."},
        {"name": "Subtraction", "equation": "5 - 3", "result": 5 - 3, "description": "Finding the difference between two numbers."},
        {"name": "Multiplication", "equation": "5 * 3", "result": 5 * 3, "description": "Adding a number to itself a specified number of times."},
        {"name": "Division", "equation": "6 / 3", "result": 6 / 3, "description": "Splitting a number into equal parts."},
        {"name": "Square Root", "equation": "sqrt(16)", "result": math.sqrt(16), "description": "Finding a number that, when squared, gives the original."},
        {"name": "Exponentiation", "equation": "2 ** 3", "result": 2 ** 3, "description": "Raising a number to the power of another number."},
        {"name": "Logarithm", "equation": "log(100, 10)", "result": math.log(100, 10), "description": "Inverse operation to exponentiation."},
        {"name": "Factorial", "equation": "factorial(5)", "result": math.factorial(5), "description": "Product of all positive integers up to a given number."},
    ]
    
    # Sort functions based on the result value
    functions.sort(key=lambda x: x["result"])

    # Calculate maximum width of the equation part for alignment
    max_equation_length = max(len(f["equation"]) for f in functions)

    # Display results in the desired format
    print("Mathematical Functions Test Results (Sorted by Result):\n")
    for func in functions:
        # Format the output so that the equation and description are aligned
        equation = f"Equation: {func['equation']} = {func['result']}"
        description = func['description']
        
        # Adjust spacing for description to align with the maximum equation length
        print(f"{equation.ljust(max_equation_length + 20)} # {description}")

# Run the function to test the math functions
if __name__ == "__main__":
    test_functions()
```

CMD: python3 PyObfuscate.py PyMathDemo.py --hex --compress --split
```python
# Obfuscated loader generated.
DATE_CREATED = "2025-05-08 01:57:00"
# Original file: PyMathDemo.py
import base64, zlib, sys
def run():
    seg0    = "789c7595cf6fdb3a0cc7eff92b38e750a7cbd276c3760890c3b0aec003de80a1ddad0b0cc5a663bd"
    seg1    = "674b9e24270d8afeef23e51f711ca787a0a628f2a32f456afaeea6b2e66623d50daa1d94079769f5"
    seg2    = "69228b521b07857019004ce15786f5472e374698039446ef6482d65b917e642c72482b153ba99505"
    seg3    = "a11288e91f2794b360ab380361c119b9d54a1748ffc473c8f55618e9b2823f7887a6580644b2132a"
    seg4    = "c6e434b62ed1081f7c31994ce11e53a9102c05abc98eb9f71412882d36b2f49649822938b42eea9c"
    seg5    = "c2d9724227ebed5ac1b3b7f0df6ba04481c11282af4922793d9843807f2a0fc0f6cff01e3eb1d1a0"
    seg6    = "ad7247266f21432f313b7ed305892bd516dc5e8336506883a0aa62838604d1b0450782142a16c1db"
    seg7    = "7c84e0a9da3823e271880f67101fc6201ea44a3c02953191698a064960d8a0db232a4fd6105d80f8"
    seg8    = "41e165995321c639aecf38aec738584dc2104d363ebe7416f39415283196a9a4b2378b9a6a260bbc"
    seg9    = "84742f77d28ec07c819b018cb79cc33cd1799c3be1918a8838580ea530ee52ea27f2a0223e6aed86"
    seg10   = "d9ed1fe3c2bb2fb31300be9f8b76e572758eb264c2cd619f5169ac4f95cc612b77d46d5c404d4d24"
    seg11   = "95c82fc07d7f29b542e5e468a93ec2f5b056b5e91ceb5190be836a71fe52efebea0855f76bbd7c01"
    seg12   = "e7dfb6c78724d4fce1ddeded1cee6e47d4eaaf9ea3fda3767457f13813980d4f0e7e01e7813a8904"
    seg13   = "14f910276d17c2cf2338fdd5739c9f462755ecbc26395d1d6d6966ec90af136eb9cdab9201852fa2"
    seg14   = "1aeab5f6bffe670a4f3c768f4369232c35049f8f84af916027f20a4f87d7c2d2b6f07f3cac72516c"
    seg15   = "12012f4b78796ecfb09e4d9ae8df441e57b9703c325f645115342b131a96dc6a94a0d5c35f7e4869"
    seg16   = "58895c6e5541a2fa00b4296a7da21cd596b6aed81ad247983e1f055dcffcf6942438527618f7d296"
    seg17   = "b9383407b2ece427135a49779d7792e8deb734a46118fce83f040f9d3abf68a4c363132464e968f7"
    seg18   = "e6d09866cbdf2a98d542310b6d3bc15976d7630a0f3e65dd5e952b2b470f8b6fc3535df88dead51e"
    seg19   = "780a788930e98275ce2b4883efcdc7125e39eff355bb7ab57e2387c658eb40a6a08bd2cfb282daad"
    seg20   = "67bb5a779ebd537c4dfeab48115b8a981b974fdd8fc3579061eb07d265c75bd031d745ed42d6f2a7"
    seg21   = "c16bebb0c83943387611dec3c7dbd91b51bcf672be5101e8b17eacea0ab7dafb51c2c573d9f0f59e"
    seg22   = "c814a288db358a60b582208a0a2155140575bd86cff8e42f48c6d6de"
    segments = [locals()[f"seg{i}"] for i in range(23)]
    PyFile = bytes.fromhex("".join(segments))
    PyFile = zlib.decompress(PyFile)
    exec(PyFile.decode("utf-8"), globals())

if __name__ == "__main__":
    run()
```

CMD: python3 PyObfuscate.py PyMathDemo.py --hex --compress --split -O demo.py

[+] Obfuscated loader written to demo.py

CMD: python3 demo.py
```python
Mathematical Functions Test Results (Sorted by Result):

Equation: 5 - 3 = 2              # Finding the difference between two numbers.
Equation: 6 / 3 = 2.0            # Splitting a number into equal parts.
Equation: log(100, 10) = 2.0     # Inverse operation to exponentiation.
Equation: sqrt(16) = 4.0         # Finding a number that, when squared, gives the original.
Equation: 5 + 3 = 8              # Combining two or more numbers to get a sum.
Equation: 2 ** 3 = 8             # Raising a number to the power of another number.
Equation: 5 * 3 = 15             # Adding a number to itself a specified number of times.
Equation: factorial(5) = 120     # Product of all positive integers up to a given number.
```


### Notes

* The generated loader script is self-contained and can be executed without requiring external libraries.
* Ensure you store your XOR encryption keys securely. It is not inteded to be secure as much as Obfuscated.
* The self-test feature can help verify that the obfuscated code still works after being transformed.

## Versioning

This script uses semantic versioning. The current version is `1.5.0`.

## Licensing

This suite is released under the [MIT License](LICENSE.md).

## Disclaimer

This script is intended for educational and testing purposes. Please ensure you comply with all relevant laws and guidelines when using it.
