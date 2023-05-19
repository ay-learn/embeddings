#!/usr/bin/env python3
import argparse
import os

from add_emb import add_to_database


def list_files(dir):
    """Returns a list of all files in the given directory and its subdirectories"""
    files = []
    extensions = [
        ".bash",
        ".bib",
        ".c",
        ".cpp",
        ".html",
        ".js",
        ".lua",
        ".md",
        ".py",
        ".rmd",
        ".sh",
        ".tex",
        ".txt",
        ".typ",
    ]

    # extensions = [".md"]

    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            # check if file is not empty
            if os.path.getsize(filepath) > 0:
                if filename.endswith(tuple(extensions)):
                    files.append(filepath)
    return files


def main():
    parser = argparse.ArgumentParser(description="List all files in a directory")
    parser.add_argument("dir", type=str, help="Path to directory")
    args = parser.parse_args()

    # Check if the directory exists
    if not os.path.isdir(args.dir):
        print(f"Directory '{args.dir}' not found.")
        return

    # List and print all files in the directory
    files = list_files(args.dir)
    print(f"There are {len(files)} files in '{args.dir}':")
    for i, file in enumerate(files):
        print(f"{i+1}/{len(files)}: {file}")
        add_to_database(file)


if __name__ == "__main__":
    main()
