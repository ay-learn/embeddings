#!/usr/bin/env python3
import argparse
import os
import pathlib

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import LatexTextSplitter
from langchain.text_splitter import MarkdownTextSplitter
from langchain.text_splitter import PythonCodeTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from HistoryDB import append_file
from HistoryDB import get_processed_files
from HistoryDB import processed
# from langchain.document_loaders import TextLoader

# from langchain.embeddings.openai import OpenAIEmbeddings



def create_database(docs):
    persist_directory = "/data/projects/embedding/hf3"
    parent_directory = os.path.dirname(persist_directory)

    if not os.path.exists(parent_directory):
        print("Parent directory does not exist!")
        return

    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings()
    # Embed and store the texts
    vectordb = Chroma.from_documents(
        documents=docs, embedding=embeddings, persist_directory=persist_directory
    )
    vectordb.persist()


def add_to_database(file):
    filename = file
    file = pathlib.Path(file).read_text()
    if file.endswith(".py"):
        python_splitter = PythonCodeTextSplitter(chunk_size=30, chunk_overlap=0)
        docs = python_splitter.create_documents([file])
    if file.endswith(".tex"):
        latex_splitter = LatexTextSplitter(chunk_size=400, chunk_overlap=0)
        docs = latex_splitter.create_documents([file])
    if file.endswith(".md"):
        markdown_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=50)
        docs = markdown_splitter.create_documents([file])
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=200,
            chunk_overlap=20,
            length_function=len,
        )

        docs = text_splitter.create_documents([file])
    try:
        create_database(docs)
        processed_files=get_processed_files("file.db")
        append_file(filename, "file.db", processed_files)
    except Exception as e:
        print(f"An error occurred while persisting the vectordb: {e}")
    print("---")


def main():
    parser = argparse.ArgumentParser(description="Embedding this file")
    parser.add_argument("file", type=str, nargs="?", help="Path to file")
    args = parser.parse_args()
    if args.file is None:
        print("Please provide the file path")
        return

    else:
        if not os.path.isfile(args.file):
            print(f"File '{args.file}' not found.")
            return

    processed_files = get_processed_files("file.db")
    # tracing lsit of files
    # print(processed_files)
    # print(processed(args.file, processed_files))

    if not processed(args.file, processed_files):
        add_to_database(args.file)
    else:
        print(f"already embedded {args.file}")


if __name__ == "__main__":
    main()
