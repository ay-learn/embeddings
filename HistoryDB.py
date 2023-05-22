#!/usr/bin/env python3
import argparse
import os

from pathlib import Path

def processed(file, processed_files):
    file = Path(file).absolute()
    # print(file)
    return str(file) in processed_files


def append_file(file, db, processed_files):
    file = Path(file).absolute()
    # Use the with statement to ensure the file is closed properly
    with open(db, "a") as f:  # Use append mode instead of write mode
        f.write(str(file) + "\n")  # Write the file name to the database file
    processed_files.append(file)  # Update the processed_files list


def get_processed_files(db):
    processed_files = []
    if os.path.exists(db):
        with open(db, "r") as f:
            processed_files = f.read().splitlines()
    # print(processed_files)
    return processed_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="the file to process")
    parser.add_argument("-d", "--db", help="the database file")
    args = parser.parse_args()

    if args.file is None:
        print("add a file to process it")
        exit(1)

    if args.db is None:
        print("add the database file name")
        exit(1)

    file = args.file
    db = args.db

    processed_files = get_processed_files(db)

    if not processed(file, processed_files):
        append_file(file, db, processed_files)


if __name__ == "__main__":
    main()
