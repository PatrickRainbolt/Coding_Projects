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

## Licensing

This suite is released under the [MIT License](LICENSE.md).
