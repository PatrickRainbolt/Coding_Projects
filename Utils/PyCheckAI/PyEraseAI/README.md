# Watermark Removal Tool

This Python script removes watermark-related keywords and invisible characters from documents and raw text. It supports processing \`.txt\`, \`.docx\`, and \`.pdf\` files, as well as handling raw text input.

## Features

* **Removes Watermark Keywords:** Eliminates common watermark keywords (e.g., "watermark", "confidential", "draft") from the text.
* **Removes Invisible Characters:** Strips out zero-width characters (e.g., zero-width spaces) that are often used for invisible watermarking.
* **File Processing:** Can process text from \`.txt\`, \`.docx\`, and \`.pdf\` files.
* **Raw Text Input:** Accepts raw text as input via standard input (stdin).
* **Command-Line Interface:** Provides a simple command-line interface for easy use.
* **Version Display:** Includes a `-V` or `--version` flag to display the script's version.

## Requirements

* Python 3.x
* Third-party libraries:
    * `python-docx`
    * `PyPDF2`

## Installation

1.  Ensure you have Python 3.x installed.
2.  Install the required third-party libraries using pip:

    ```bash
    pip install python-docx PyPDF2
    ```

## Usage

###   Command-Line Arguments

The script is executed from the command line:

```bash
python PyEraseAI.py [options] [file]
file (optional):  The path to the document file you want to process.  Supported formats are `.txt`, `.docx`, and `.pdf`.options:-V, --version:  Display the script's version number and exit.--raw:  Read raw text from standard input (stdin).  If this option is used, the file argument is ignored.ExamplesProcess a `.txt` file:python PyEraseAI.py document.txt
Process a `.docx` file:python PyEraseAI.py document.docx
Process a `.pdf` file:python PyEraseAI.py document.pdf
Process raw text from stdin (e.g., using a pipe):cat text_file.txt | python PyEraseAI.py --raw
Display the script's version:python PyEraseAI.py --version
OutputThe script will either print the cleaned text to standard output (if using the --raw option) or save the cleaned text to a new file named clean_<original_filename>.txt in the same directory as the original file.  The script will also print the name of the cleaned output file.Script DetailsThe script performs the following main steps:Imports Libraries: Imports necessary standard library modules (os, sys, re, argparse) and the third-party libraries (docx, PyPDF2).Defines Constants:VERSION:  The script's version number.zero_width_chars:  A list of zero-width Unicode characters to be removed.watermark_keywords:  A list of watermark keywords (case-insensitive) to be removed.clean_text(text) Function:Takes a text string as input.Removes zero-width characters.Removes watermark keywords using a regular expression.Returns the cleaned text.clean_txt(file_path), clean_docx(file_path), clean_pdf(file_path) Functions:These functions handle the extraction of text from the respective file formats and then use the clean_text() function to clean the extracted text.save_cleaned_text(text, original_path) Function:Saves the cleaned text to a new text file.Constructs the output filename.Prints a message indicating the name of the saved file.main() Function:Parses command-line arguments using argparse.Handles the --raw option: reads from stdin, cleans the text, and prints to stdout.Handles file input:Determines the file type based on the extension.Calls the appropriate cleaning function (clean_txt(), clean_docx(), clean_pdf()).
