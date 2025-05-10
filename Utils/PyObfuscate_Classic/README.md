# PyObfuscate_Classic

`PyObfuscate_Classic.py` is a simple Python 3 script designed for basic obfuscation of other Python scripts. It works by parsing the input script's Abstract Syntax Tree (AST) and renaming variables and functions to short, random strings. It also includes experimental features for combining imports and basic code "flattening".

**Disclaimer:** This is a basic obfuscator and should not be considered cryptographically secure or suitable for protecting sensitive code from determined analysis. It primarily serves to make code less immediately readable.

## Features

* **Variable Renaming:** Renames local variables and function arguments to random strings.
* **Function Renaming:** Renames function definitions and calls to random strings.
* **AST-Based:** Operates by transforming the code's Abstract Syntax Tree, which is generally more robust than regex-based methods for renaming within scope.
* **Import Combining (`-F` flag):** Attempts to consolidate multiple `import` statements into a single line (part of the flattening process).
* **Basic Flattening (`-F` flag):** Attempts to compress function bodies onto fewer lines using semicolons. **Note:** This feature is experimental and may produce syntactically invalid code for complex function bodies.

## Requirements

* Python 3.6+ (due to f-strings and AST structure assumptions)

## Usage

```bash
python3 PyObfuscate_Classic.py <input_file> [options]
```

**Arguments:**

* `<input_file>`: The path to the Python file you want to obfuscate (required).

**Options:**

* `-O <filename>`, `--outfile <filename>`: Write the obfuscated code to the specified file.
* `-p`, `--print`: Print the obfuscated code directly to the console (stdout).
* `-F`, `--flatten`: Apply experimental flattening techniques (combine imports, compress functions). **Use with caution.**
* `-V`, `--VERSION`: Show the version of the obfuscator and exit.

If no output option (`-O` or `-p`) is provided, the obfuscated code will be printed to the console by default (unless `-F` is used, in which case the output behavior without `-O` or `-p` is governed by the `elif not print_to_screen and not output_file:` block in the script).

## Examples

Obfuscate `my_script.py` and save to `obfuscated_script.py`:

```bash
python3 PyObfuscate_Classic.py my_script.py -O obfuscated_script.py
```

Obfuscate `my_script.py`, apply flattening, and save to `obfuscated_script.py`:

```bash
python3 PyObfuscate_Classic.py my_script.py -F -O obfuscated_script.py
```

Show the version:

```bash
python3 PyObfuscate_Classic.py -V
```

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

CMD: python3 PyObfuscate_Classic.py PyMathDemo.py -F
```python
#!/usr/bin/env python3
# Python Code Obfuscated on 2025-05-10 00:49:34:

import argparse, grp, os, pwd, stat, time
wuegsnv = '1.0.0'

def mw0wx3g3(ftylyq):
    rogpath = os.lstat(ftylyq); eqfwxffaan = stat.filemode(rogpath.st_mode); xedszucxql = rogpath.st_nlink; lkqnblhc = pwd.getpwuid(rogpath.st_uid).pw_name; issxw = grp.getgrgid(rogpath.st_gid).gr_name; ccjpffwbm = rogpath.st_size; oahawwojac = time.strftime('%b %e %H:%M', time.localtime(rogpath.st_mtime)); return f'[{eqfwxffaan} {xedszucxql} {lkqnblhc} {issxw:8} {ccjpffwbm:6} {oahawwojac}]'

def p70a2j10tj(ftylyq, zycyosfu=''):
    vqgaeszp = sorted(os.listdir(ftylyq)); nxbgbvajdu = (len(vqgaeszp) - 1)
    for (serfav, pjgere) in enumerate(vqgaeszp):
        rhaen = os.path.join(ftylyq, pjgere); fbhxcmmshq = (serfav == nxbgbvajdu); zofyplshoo = ('└── ' if fbhxcmmshq else '├── '); mwtldvpu = ((zycyosfu + zofyplshoo) + pjgere); ymmpjylem = mw0wx3g3(rhaen); print(f'{ymmpjylem:<60}  {mwtldvpu}')
        if (os.path.isdir(rhaen) and (not os.path.islink(rhaen))):
            opwvafoz = ('    ' if fbhxcmmshq else '│   '); p70a2j10tj(rhaen, (zycyosfu + opwvafoz))
if (__name__ == '__main__'):
    yovtix = argparse.ArgumentParser(description='Tree view with detailed file info')
    yovtix.add_argument('path', help='Root path to start tree from')
    yovtix.add_argument('-H', '--HEADERS', action='store_true', help='Show column headers')
    yovtix.add_argument('-V', '--VERSION', action='version', version=f'%(prog)s {wuegsnv}', help='Show version number')
    qxyxqpwycu = yovtix.parse_args()
    devgwhfdik = os.path.abspath(qxyxqpwycu.path)
    if qxyxqpwycu.HEADERS:
        print(f"{'   Perms   Lnk  Owner  Group    Size   Date  Time':<60}   {'Path'}")
        print(f"{('-' * 60)}  {('-' * 40)}")
    cbofpbiliw = mw0wx3g3(devgwhfdik)
    print(f'{cbofpbiliw:<60}  {os.path.basename(devgwhfdik)}')
    p70a2j10tj(devgwhfdik)

```

CMD: python3 PyObfuscate_Classic.py PyMathDemo.py -F -O demo.py

[+] Obfuscated code written to demo.py

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

## Version

Current version: 1.0.1

## Licensing

This suite is released under the [MIT License](LICENSE.md).
