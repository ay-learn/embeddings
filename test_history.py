#!/usr/bin/env python3

# import os
# import argparse

from pathlib import Path

from HistoryDB import processed, get_processed_files, append_file

def main():
    print("---")

    processed_files=get_processed_files("file.db")
    file=Path("build/prompt04.md").absolute()
    if processed(file,processed_files):
        print(f" exsit {file}")
    else:
        print(f" not exsit {file}")

    file=Path("build/prompt05.md").absolute()
    append_file(file,"file.db",processed_files)

if __name__ == "__main__":
    main()
