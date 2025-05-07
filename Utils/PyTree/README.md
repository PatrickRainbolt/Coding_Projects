# PyTree

`PyTree` is a Python script that provides a detailed view of files and directories, displaying file permissions, owner, group, size, and modification time, in a tree-like structure. It allows users to view file information for a given directory recursively and offers options to display headers, version info, and customize the root directory.

## Features

- **Recursive File Tree**: Displays the tree structure of directories and files starting from the specified root.
- **File Information**: For each file and directory, it shows the permissions, number of links, owner, group, size, and last modified date.
- **Command-Line Options**:
  - `-H` or `--HEADERS`: Display column headers for the output.
  - `-V` or `--VERSION`: Display the version of the script.
- **Customizable Root Directory**: Start the file tree view from any specified directory path.

## Requirements

This script requires Python 3.x and the following standard libraries:
- `os`: To perform system-level operations like listing files and directories.
- `stat`: To interpret file permissions.
- `pwd`: To get the user details based on user ID.
- `grp`: To get the group details based on group ID.
- `time`: To format file modification timestamps.
- `argparse`: To handle command-line arguments.

## Installation

### 1. Ensure Python 3 is Installed

Ensure Python 3.x is installed on your system. You can check by running:

```bash
python3 --version
```

If not installed, follow the instructions for your operating system from the official [Python website](https://www.python.org/downloads/).

### 2. Run the Script

After downloading the script, you can run it directly using Python 3.

## Usage

### Basic Command

To display the tree structure for a directory and its subdirectories:

```bash
python3 tree_info.py /path/to/directory
```

### Show Version

To display the version of the script:

```bash
python3 PyTree.py -V
# or
python3 PyTree.py --VERSION
```

### Show Headers

To display headers above the tree structure:

```bash
python3 PyTree.py /path/to/directory -H
# or
python3 PyTree.py /path/to/directory --HEADERS
```

### Show Headers and Version Together

You can combine flags to show both the headers and the version:

```bash
python3 PyTree.py /path/to/directory -H -V
```

### Example Output

```bash
$ python3 PyTree.py /home/user/Documents -H

    Perms  Lnk Owner   Group   Size    Date  Time              Path
------------------------------------------------------------  ----------------------------------------
[drwxr-xr-x 5 user    user       4096 May  4 10:10]            Documents
[drwxr-xr-x 2 user    user       4096 May  4 10:12]            ├── Work
[-rw-r--r-- 1 user    user    1048576 May  3 14:30]            │   ├── work_file.txt
[-rw-r--r-- 1 user    user       2048 May  3 14:31]            │   └── work_image.jpg
[drwxr-xr-x 3 user    user       4096 May  2 15:10]            └── Personal
[-rw-r--r-- 1 user    user        512 May  1 10:15]                ├── personal_notes.txt
[-rw-r--r-- 1 user    user       1024 May  2 15:12]                └── personal_image.png
```

### Output Format

* **Perms**: File permissions (e.g., `drwxr-xr-x`).
* **Lnk**: Number of hard links.
* **Owner**: The username of the file's owner.
* **Group**: The group to which the file belongs.
* **Size**: Size of the file in bytes.
* **Date and Time**: The last modified date and time of the file.
* **Path**: The full path of the file or directory.

### Flags

* `-H` or `--HEADERS`: Display headers for the columns in the output.
* `-V` or `--VERSION`: Display the version of the script.

## Licensing

This suite is released under the [MIT License](LICENSE.md).
