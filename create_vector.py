import os

from rag.pdf_loader import load_documents
from rag.text_splitter import split_documents
from rag.embeddings import create_vector_store

documents = load_documents()

chunks = split_documents(documents)
count = 0

for chunk in chunks:

    if chunk.metadata.get("article") == "21":

        print("=" * 80)
        print(chunk.metadata)
        print(chunk.page_content[:1000])
        count += 1

print("Total Article 21 Chunks:", count)

print("\nChecking Constitution article metadata...\n")

count = 0

for chunk in chunks:
    if chunk.metadata.get("article"):
        print(chunk.metadata)
        print(chunk.page_content[:150])
        print("-" * 60)

        count += 1

        if count == 20:
            break

print(f"\nTotal chunks with article metadata: {count}")
print("-" * 50)
print(f"\nTotal Chunks: {len(chunks)}")

if len(chunks) > 0:
    print("\nFirst Chunk:")
    print(chunks[0].page_content[:500])
    print(chunks[0].metadata)

create_vector_store(chunks)

print("✅ Vector DB Created")