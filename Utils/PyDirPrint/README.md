# PyDirPrint

**PyDirPrint** is a versatile Python script designed to traverse directories and display detailed information about files. It offers various features to customize the output, including viewing file metadata, filtering files by name, and redirecting output to a file.

## Features

- **Display File Metadata**: Use the `-H` or `--HEADER` flag to display detailed file metadata, similar to what you would fine in the output of `ls -l`.
- **Search Files by Name**: Use the `-S` or `--SEARCH` flag followed by a pattern to filter files by name using shell-style wildcards (e.g., `*.txt`).
- **Redirect Output to File**: Use the `-O` or `--OUTFILE` flag followed by a filename to redirect the output to a file. The output will only be written if matching files are found.
- **Show Version**: Use the `-V` or `--VERSION` flag to display the script's version number.

## Installation

Ensure you have Python 3 installed. No additional installation is required for the script itself.

## Usage

```bash
python3 PyDirPrint.py <directory> [options]
````

### Options

* `-H`, `--HEADER`: Display detailed file metadata.
* `-S <pattern>`, `--SEARCH=<pattern>`: Filter files by name using shell-style wildcards.
* `-O <filename>`, `--OUTFILE=<filename>`: Redirect output to a file. Output is written only if matching files are found.
* `-V`, `--VERSION`: Display the script's version number.

### Examples

1. **Display file metadata for all files in a directory**:

   ```bash
   python3 PyDirPrint.py /path/to/directory -H
   ```

2. **Filter and display `.txt` files**:

   ```bash
   python3 PyDirPrint.py /path/to/directory -S "*.txt"
   ```

3. **Redirect output to a file**:

   ```bash
   python3 PyDirPrint.py /path/to/directory -O output.txt
   ```

4. **Display version number**:

   ```bash
   python3 PyDirPrint.py -V
   ```

## Example of Output
   ```bash
> python3 PyDirPrint.py Coding -S '*.txt'

------------------------------------------------------------------------------------------
[-rw-rw-r-- 1 digipat digipat  1024 May  7 10:14] /home/user/Coding/Fibonacci_Sequence.txt
------------------------------------------------------------------------------------------
The Fibonacci sequence is a series of numbers in which each number is the sum of the two preceding ones. It commonly
starts with 0 and 1. This sequence appears in many areas of mathematics and computer science, as well as in nature,
such as the arrangement of leaves or the spirals of shells.

In Python, the Fibonacci sequence can be implemented in several ways. A common method is using iteration with a loop,
where two variables track the previous values and are updated as the loop progresses. Another method is using
recursion, where a function calls itself with smaller inputs to build the sequence. Recursion is elegant but less
efficient for large inputs unless memoization is used.

Here is an example of a simple iterative Fibonacci generator in Python:
   def fibonacci(n):
       a, b = 0, 1
       for _ in range(n):
           print(a, end=' ')
           a, b = b, a + b
   ```

## Licensing

This suite is released under the [MIT License](LICENSE.md).
