# Standard library imports
import os             # Provides a way to interact with the operating system (e.g., file paths, directories).
import sys            # Provides access to system-specific parameters and functions (e.g., command-line arguments).
import re             # Provides support for regular expressions to search, match, or replace patterns in strings.
import argparse       # A command-line argument parsing library, useful for handling input arguments from the command line.
from collections import Counter  # A specialized dictionary class from the collections module to count hashable objects.

# Third-party library imports
from docx import Document  # docx is a third-party library to handle .docx Word documents.
from PyPDF2 import PdfReader  # PyPDF2 is a third-party library to extract text from PDF files.

# Define the version of the program
VERSION = "1.0.0"

# Define Unicode for special watermark characters (invisible characters)
zero_width_chars = [
    '\u200B',  # Zero-Width Space (ZWSP)
    '\u200C',  # Zero-Width Non-Joiner (ZWNJ)
    '\u200D',  # Zero-Width Joiner (ZWJ)
    '\uFEFF',  # Zero-Width No-Break Space (ZWNBSP)
]

# Function to extract text from .txt files
def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to extract text from .docx files
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Function to extract text from .pdf files
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to count watermark-related keywords in extracted text
def count_watermarks(text):
    # Define common watermark keywords
    watermark_keywords = ['watermark', 'confidential', 'do not copy', 'sample', 'draft', 'copyright']

    # Convert text to lowercase and split into words
    words = re.findall(r'\w+', text.lower())
    
    # Count watermark-related keywords
    watermark_counts = Counter()
    
    for word in words:
        if word in watermark_keywords:
            watermark_counts[word] += 1
    
    return watermark_counts

# Function to count invisible characters used in watermarking
def count_zero_width(text):
    count = 0
    for char in zero_width_chars:
        count += text.count(char)
    return count

# Function to scan the document for watermarks
def scan_document(file_path=None, file_type=None, raw_input=None):
    # If raw_input is provided, use it, otherwise, process the file
    if raw_input:
        text = raw_input
    else:
        # If no file_type is provided, rely on the file extension
        if file_type is None and file_path:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
        else:
            ext = file_type

        # Extract text based on file type
        if ext == '.txt' or file_type == 'txt':
            text = extract_text_from_txt(file_path)
        elif ext == '.docx' or file_type == 'docx':
            text = extract_text_from_docx(file_path)
        elif ext == '.pdf' or file_type == 'pdf':
            text = extract_text_from_pdf(file_path)
        else:
            print(f"Unsupported file type: {ext}")
            return

    # Count the watermarks in the extracted text
    watermark_counts = count_watermarks(text)

    # Count zero-width characters as part of watermark detection
    zero_width_count = count_zero_width(text)

    # Print the results in a more professional format
#    print("\n=============================== Watermark Detection ===============================\n")

    if watermark_counts or zero_width_count > 0:
        print(f"\nWatermark Summary:\n")
        print(f"{'Keyword':<40}{'Count'}")
        print("-" * 50)
        for watermark, count in watermark_counts.items():
            print(f"* {watermark.capitalize():<38}{count}")
#        print("-" * 50)
        
        print(f"\nZero-Width:\n")
        print(f"{'Keyword':<40}{'Count'}")
        print("-" * 50)
        
        print(f"{'* Characters Detected:':<40}{zero_width_count}")
#        print("-" * 50)

        total_watermarks = sum(watermark_counts.values()) + zero_width_count
        print(f"\nTotal Watermarks Detected (including invisible characters): {total_watermarks}\n")
    else:
        print("No watermarks found.\n")

#    print("\n=====================================================================================\n")

# Main function to handle command-line input and options
def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Scan documents or raw text for watermark-like keywords, including invisible characters.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the document file (txt, docx, or pdf). If --raw is used, this is ignored."
    )

    # Optional arguments for specifying the file type manually
    parser.add_argument(
        "--txt",
        action="store_true",
        help="Force the file to be treated as a plain text file (.txt)."
    )
    parser.add_argument(
        "--docx",
        action="store_true",
        help="Force the file to be treated as a Word document (.docx)."
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Force the file to be treated as a PDF file (.pdf)."
    )

    # --raw option for accepting piped input
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Accept raw text input from stdin (piped data)."
    )

    # --version option to display the version
    parser.add_argument(
        "-V", "--version",
        action="version", 
        version=f"%(prog)s {VERSION}",
        help="Show program's version number and exit."
    )

    # Parse arguments
    args = parser.parse_args()

    # Check if raw input is being used
    if args.raw:
        # Read raw input from stdin (pipe)
        raw_input = sys.stdin.read()
        scan_document(raw_input=raw_input)
    else:
        # Otherwise, process the file as usual
        file_type = None
        if args.txt:
            file_type = 'txt'
        elif args.docx:
            file_type = 'docx'
        elif args.pdf:
            file_type = 'pdf'

        if args.file:
            scan_document(args.file, file_type)
        else:
            print("Error: No file or raw input specified. Use --help for usage instructions.")
            sys.exit(1)

if __name__ == "__main__":
    main()
