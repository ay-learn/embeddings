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
    processed_files = get_processed_files("file.db")
    if processed(file, processed_files):
        print(f"already embedded {file}")
        # remove it
        # return

    file = pathlib.Path(file).read_text()
    if filename.endswith(".py"):
        print("py files")
        python_splitter = PythonCodeTextSplitter(chunk_size=200, chunk_overlap=0)
        docs = python_splitter.create_documents([file])
    if filename.endswith(".tex"):
        print("tex files")
        latex_splitter = LatexTextSplitter(chunk_size=500, chunk_overlap=0)
        docs = latex_splitter.create_documents([file])
    if filename.endswith(".md"):
        print("md files")
        markdown_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=50)
        docs = markdown_splitter.create_documents([file])
    else:
        print("else files")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=20,
            length_function=len,
        )

        docs = text_splitter.create_documents([file])
    try:
        create_database(docs)
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

    add_to_database(args.file)


if __name__ == "__main__":
    main()
