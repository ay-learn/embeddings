#!/usr/bin/env python3
import argparse
import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def vec_database(persist_directory,query):
    embedding = OpenAIEmbeddings()
    # Load the persisted database from disk.
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return vectordb.similarity_search(query)

def query_database(query):
    persist_directory = "/data/projects/embedding/db"
    parent_directory = os.path.dirname(persist_directory)

    if not os.path.exists(parent_directory):
        print("Parent directory does not exist!")
        return


    # hide some stdoutput
    # TODO: what if failed to connect with db/internel/api
    import contextlib
    with contextlib.redirect_stdout(None):
        docs = vec_database(persist_directory,query)

    return docs[0].page_content


def main():
    parser = argparse.ArgumentParser(description="Embedding this file")
    parser.add_argument("query", type=str, nargs="?", help="Query embedding")
    args = parser.parse_args()
    if args.query is None:
        print("Please provide the query text")
        return

    answer = query_database(args.query)
    print(answer)


if __name__ == "__main__":
    main()
