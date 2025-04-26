# Watermark Detection Tool

This Python script scans documents (including \`.txt\`, \`.docx\`, and \`.pdf\` formats) for watermark-like keywords and invisible characters that may be used for watermarking. It can detect standard visible watermarks as well as invisible zero-width characters.

## Features

* Extracts text from \`.txt\`, \`.docx\`, and \`.pdf\` files.
* Searches for common watermark keywords such as "watermark", "confidential", "draft", etc.
* Detects invisible characters commonly used in watermarking, including zero-width spaces and other special Unicode characters.
* Supports raw text input via the command line.
* Provides a version flag to check the current version of the tool.

## Requirements

* Python 3.x
* Required libraries:
    * `argparse` (Standard Library)
    * `re` (Standard Library)
    * `sys` (Standard Library)
    * `os` (Standard Library)
    * `collections` (Standard Library)
    * `python-docx` (Third-party library to handle \`.docx\` files)
    * `PyPDF2` (Third-party library to handle \`.pdf\` files)

To install the required Python libraries, you can use `pip`:

\`\`\`bash
pip install python-docx PyPDF2
\`\`\`

## Installation

Clone or download this repository to your local machine.

Install the required Python libraries (see above).

Ensure you are using Python 3.x and have the necessary permissions to execute Python scripts.

## Usage

### Basic Usage

To use the watermark detection tool, run the script from the command line:

\`\`\`bash
python watermark_detection.py \[OPTIONS\] <file_path>
\`\`\`

Where `<file_path>` is the path to the document file you want to scan.

### Options

* `-V`, `--version`: Displays the current version of the tool.
* `--txt`: Forces the tool to treat the input file as a plain text file (.txt).
* `--docx`: Forces the tool to treat the input file as a Word document (.docx).
* `--pdf`: Forces the tool to treat the input file as a PDF file (.pdf).
* `--raw`: Accepts raw text input (piped data from stdin).

### Example 1: Scan a .txt file for watermarks

\`\`\`bash
python watermark_detection.py --txt document.txt
\`\`\`

### Example 2: Scan a .docx file for watermarks

\`\`\`bash
python watermark_detection.py --docx document.docx
\`\`\`

### Example 3: Scan a .pdf file for watermarks

\`\`\`bash
python watermark_detection.py --pdf document.pdf
\`\`\`

### Example 4: Use raw text input (from a pipe or redirected file)

\`\`\`bash
echo "This document contains a watermark." | python watermark_detection.py --raw
\`\`\`

### Example 5: Show the version of the tool

\`\`\`bash
python watermark_detection.py --version
\`\`\`

This will output something like:

```
watermark_detection.py 1.0.0
```

## Output

The program will display a summary of detected watermarks, including:

* **Keyword-based Watermarks**: A list of common watermark keywords and their counts.
* **Invisible Characters**: A count of invisible characters (e.g., zero-width space, non-joiner, joiner, and no-break space).

If no watermarks are found, the program will display:

```
No watermarks found.
```

If watermarks are detected, the output will look like this:

```
Watermark Summary:

Keyword                         Count
\--------------------------------------------------
\* watermark                       3
\* confidential                   2

Zero-Width:

Keyword                         Count
\--------------------------------------------------
\* Characters Detected:           5

Total Watermarks Detected (including invisible characters): 10
```

## License

This tool is licensed under the MIT License.

## Contributing

If you'd like to contribute to this project, feel free to submit issues or pull requests. Contributions are welcome!

## Author

This project was created by \[Your Name].
