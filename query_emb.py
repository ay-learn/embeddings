#!/usr/bin/env python3
import argparse
import asyncio
import contextlib
import os

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# from langchain.embeddings.openai import OpenAIEmbeddings


async def query_database(query, persist_directory):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings()
    # Load the persisted database from disk.
    vectordb = Chroma(
        persist_directory=persist_directory, embedding_function=embeddings
    )
    docs = vectordb.similarity_search(query)
    # docs = vectordb.search(query,"similarity")
    # print(docs)
    # for prevent some stdout lazy unloading and outputing in stdout
    # vectordb = None
    # vectordb.persist()
    return docs[0].page_content
    # return "---"


def check_database(persist_directory):
    parent_directory = os.path.dirname(persist_directory)

    if not os.path.exists(parent_directory):
        print("Parent directory does not exist!")
        exit(1)


async def main():
    parser = argparse.ArgumentParser(description="Embedding this file")
    parser.add_argument("query", type=str, nargs="?", help="Query embedding")
    args = parser.parse_args()
    if args.query is None:
        print("Please provide the query text")
        return

    # hide some stdoutput
    # TODO: what if failed to connect with db/internel/api

    persist_directory = "/data/projects/embedding/hf3"
    check_database(persist_directory)

    # with contextlib.redirect_stdout(None):
    #     answer = await query_database(args.query, persist_directory)
    answer = await query_database(args.query, persist_directory)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
