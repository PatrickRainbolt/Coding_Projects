# Standard library imports
import os             # Provides a way to interact with the operating system (e.g., file paths, directories).
import sys            # Provides access to system-specific parameters and functions (e.g., command-line arguments).
import re             # Provides support for regular expressions to search, match, or replace patterns in strings.
import argparse       # A command-line argument parsing library, useful for handling input arguments from the command line.

# Third-party library imports
from docx import Document  # docx is a third-party library to handle .docx Word documents.
from PyPDF2 import PdfReader  # PyPDF2 is a third-party library to extract text from PDF files.

VERSION = "1.0.0"

# Define invisible characters often used in watermarking
zero_width_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF']

# Define watermark keywords
watermark_keywords = ['watermark', 'confidential', 'do not copy', 'sample', 'draft', 'copyright']

# Clean watermark content
def clean_text(text):
    for char in zero_width_chars:
        text = text.replace(char, '')
    pattern = re.compile(r'\b(' + '|'.join(watermark_keywords) + r')\b', re.IGNORECASE)
    return pattern.sub('', text).strip()

# Clean TXT
def clean_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return clean_text(f.read())

# Clean DOCX
def clean_docx(file_path):
    doc = Document(file_path)
    cleaned_paragraphs = [clean_text(p.text) for p in doc.paragraphs]
    return "\n".join(cleaned_paragraphs)

# Clean PDF
def clean_pdf(file_path):
    reader = PdfReader(file_path)
    cleaned_text = ""
    for page in reader.pages:
        text = page.extract_text()
        cleaned_text += clean_text(text) + "\n"
    return cleaned_text

# Save cleaned text to a .txt file
def save_cleaned_text(text, original_path):
    base, _ = os.path.splitext(os.path.basename(original_path))
    output_filename = f"clean_{base}.txt"
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.write(text)
    print(f"Cleaned file saved as: {output_filename}")

# Main CLI entry
def main():
    parser = argparse.ArgumentParser(
        description="Remove watermark-related keywords and invisible characters from documents or piped text."
    )
    parser.add_argument("file", nargs="?", help="Path to the file (.txt, .docx, .pdf)")
    parser.add_argument("--raw", action="store_true", help="Read raw text from stdin and output cleaned text")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    # Handle raw input mode
    if args.raw:
        raw_input = sys.stdin.read()
        cleaned = clean_text(raw_input)
        print(cleaned)
        return

    # Handle file-based input
    if not args.file:
        print("Error: No input file specified. Use --help for usage.")
        sys.exit(1)

    ext = os.path.splitext(args.file)[1].lower()

    if ext == '.txt':
        cleaned = clean_txt(args.file)
    elif ext == '.docx':
        cleaned = clean_docx(args.file)
    elif ext == '.pdf':
        cleaned = clean_pdf(args.file)
    else:
        print(f"Unsupported file format: {ext}")
        sys.exit(1)

    save_cleaned_text(cleaned, args.file)

if __name__ == "__main__":
    main()
