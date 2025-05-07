#!/usr/bin/env python3
import os        # for path, file, and directory operations
import stat      # for interpreting file mode/permissions
import pwd       # to get the username from a user ID
import grp       # to get the group name from a group ID
import time      # to format file modification time
import argparse  # for parsing command-line arguments

VERSION = "1.0.0"  # Global version variable

# Return a formatted string of permissions, owner, group, size, and modification time for a file.
def format_file_info(path):
    st = os.lstat(path)
    mode = stat.filemode(st.st_mode)
    nlink = st.st_nlink
    uid = pwd.getpwuid(st.st_uid).pw_name
    gid = grp.getgrgid(st.st_gid).gr_name
    size = st.st_size
    mtime = time.strftime("%b %e %H:%M", time.localtime(st.st_mtime))
    return f"[{mode} {nlink} {uid} {gid:8} {size:6} {mtime}]"

# Recursively print tree structure with file info starting from `path`.
def walk_directory(path, prefix=""):
    entries = sorted(os.listdir(path))
    last_index = len(entries) - 1

    for index, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        is_last = index == last_index
        connector = "└── " if is_last else "├── "

        tree_line = prefix + connector + entry
        info_line = format_file_info(full_path)
        print(f"{info_line:<60}  {tree_line}")

        if os.path.isdir(full_path) and not os.path.islink(full_path):
            extension = "    " if is_last else "│   "
            walk_directory(full_path, prefix + extension)

if __name__ == "__main__":
    # argparse handles command-line arguments
    parser = argparse.ArgumentParser(description="Tree view with detailed file info")
    parser.add_argument("path", help="Root path to start tree from")
    parser.add_argument("-H", "--HEADERS", action="store_true", help="Show column headers")
    parser.add_argument("-V", "--VERSION", action="version", version=f"%(prog)s {VERSION}", help="Show version number")
    args = parser.parse_args()

    root_path = os.path.abspath(args.path)

    if args.HEADERS:
        print(f"{'   Perms   Lnk  Owner  Group    Size   Date  Time':<60}   {'Path'}")
        print(f"{'-'*60}  {'-'*40}")

    root_info = format_file_info(root_path)
    print(f"{root_info:<60}  {os.path.basename(root_path)}")
    walk_directory(root_path)
