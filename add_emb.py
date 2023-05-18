#!/usr/bin/env python3
import argparse
import os

from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

# from langchain.embeddings.openai import OpenAIEmbeddings


def create_database(documents):
    persist_directory = "/data/projects/embedding/hf"
    parent_directory = os.path.dirname(persist_directory)

    if not os.path.exists(parent_directory):
        print("Parent directory does not exist!")
        return

    # TODO, return text by our type: markdown, text, pdf ...
    # text_splitter = get_from_type() : implimet this function
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings()
    # Embed and store the texts
    vectordb = Chroma.from_documents(
        documents=docs, embedding=embeddings, persist_directory=persist_directory
    )
    vectordb.persist()


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

    loader = TextLoader(args.file)
    documents = loader.load()
    create_database(documents)


if __name__ == "__main__":
    main()
