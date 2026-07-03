import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):

    chunks = []

    normal_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    for doc in documents:

        text = doc.page_content
        metadata = doc.metadata.copy()

        document_name = metadata.get("document", "").lower()

        # =====================================================
        # Constitution
        # =====================================================

        if "contitution" in document_name or "constitution" in document_name:

            pattern = r"(?=Article\s+\d+[A-Z]?)"

            parts = re.split(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            for part in parts:

                part = part.strip()

                if len(part) < 80:
                    continue

                new_metadata = metadata.copy()

                match = re.search(
                    r"Article\s+(\d+[A-Z]?)",
                    part,
                    re.IGNORECASE
                )

                if match:
                    new_metadata["article"] = match.group(1)

                chunks.append(
                    Document(
                        page_content=part,
                        metadata=new_metadata
                    )
                )

        # =====================================================
        # IPC / BNS
        # =====================================================

        elif "ipc" in document_name or "bns" in document_name:

            parts = re.split(
                r"(?=Section\s+\d+[A-Z]?)",
                text,
                flags=re.IGNORECASE
            )

            for part in parts:

                part = part.strip()

                if len(part) < 80:
                    continue

                new_metadata = metadata.copy()

                match = re.search(
                    r"Section\s+(\d+[A-Z]?)",
                    part,
                    re.IGNORECASE
                )

                if match:
                    new_metadata["section"] = match.group(1)

                chunks.append(
                    Document(
                        page_content=part,
                        metadata=new_metadata
                    )
                )

        # =====================================================
        # Other PDFs
        # =====================================================

        else:

            pieces = normal_splitter.split_documents([doc])

            chunks.extend(pieces)

    print(f"\nCreated {len(chunks)} chunks.")

    return chunks
