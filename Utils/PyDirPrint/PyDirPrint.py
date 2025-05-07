#!/usr/bin/env python3
import os          # For file and directory traversal
import mimetypes   # For guessing binary file types
import stat        # For file permission and metadata
import pwd         # To get username from UID
import grp         # To get group name from GID
import time        # For formatting timestamps
import argparse    # For command-line parsing
import contextlib  # For redirecting stdout to a file
import fnmatch     # For shell-style wildcard matching (e.g., '*.txt')

VERSION = "1.5.0"  # Global version number

# Check if a file can be read as text.
def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except Exception:
        return False

# Return formatted file metadata string (like ls -l).
def get_file_info(path):
    st = os.lstat(path)
    mode = stat.filemode(st.st_mode)
    nlink = st.st_nlink
    uid = pwd.getpwuid(st.st_uid).pw_name
    gid = grp.getgrgid(st.st_gid).gr_name
    size = st.st_size
    mtime = time.strftime("%b %e %H:%M", time.localtime(st.st_mtime))
    return f"[{mode} {nlink} {uid} {gid:8} {size:6} {mtime}]"

# Print file content or binary info with optional headers and wildcard filtering.
def print_file_info(start_dir, show_headers=False, search_pattern=None):
    found_files = 0

    for root, _, files in os.walk(start_dir):
        for name in files:
            full_path = os.path.join(root, name)

            if search_pattern and not fnmatch.fnmatch(name, search_pattern):
                continue

            found_files += 1

            header = f"{get_file_info(full_path)} {full_path}" if show_headers else full_path

            print("-" * len(header))
            print(header)
            print("-" * len(header))

            if is_text_file(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"[Error reading file: {e}]")
            else:
                mime_type, _ = mimetypes.guess_type(full_path)
                print(f"[Binary file type: {mime_type or 'Unknown'}]")

            print("\n")

    if found_files == 0:
        print("No matching files found.")

    return found_files


if __name__ == "__main__":
    # Set up command-line interface
    parser = argparse.ArgumentParser(description="Print contents and metadata of files in a directory")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("-H", "--HEADER", action="store_true", help="Display file metadata headers")
    parser.add_argument("-S", "--SEARCH", metavar="PATTERN", help="Shell-style pattern (e.g., '*.txt') to filter files")
    parser.add_argument("-O", "--OUTFILE", metavar="FILENAME", help="Write output to file")
    parser.add_argument("-V", "--VERSION", action="version", version=f"%(prog)s {VERSION}", help="Show version number and exit")
    args = parser.parse_args()

    # Validate directory and run
    if not os.path.isdir(args.directory):
        print("Error: Provided path is not a directory.")
    else:
        if args.OUTFILE:
            with open(args.OUTFILE, "w", encoding="utf-8") as f:
                with contextlib.redirect_stdout(f):
                    count = print_file_info(args.directory, show_headers=args.HEADER, search_pattern=args.SEARCH)
            if count == 0:
                # No files matched; clean up output file and notify user
                os.remove(args.OUTFILE)
                print("No matching files found.")
            else:
                print(f"{count} file(s) written to {args.OUTFILE}")
        else:
            print_file_info(args.directory, show_headers=args.HEADER, search_pattern=args.SEARCH)
