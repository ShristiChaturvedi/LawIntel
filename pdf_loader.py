import os
import re
import fitz
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")


# ==========================================================
# Clean Text
# ==========================================================

def clean_text(text: str):

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"^\d+\s*$", "", text, flags=re.MULTILINE)

    text = re.sub(
        r"THE CONSTITUTION OF INDIA",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = text.replace("\uf0b7", "")
    text = text.replace("\xa0", " ")

    return text.strip()


# ==========================================================
# Load PDFs
# ==========================================================

def load_documents():

    documents = []

    pdf_files = [
        file
        for file in os.listdir(DATA_PATH)
        if file.lower().endswith(".pdf")
    ]

    print(f"\nFound {len(pdf_files)} PDF(s).")

    for filename in pdf_files:

        path = os.path.join(DATA_PATH, filename)

        pdf = fitz.open(path)

        print(f"Loading: {filename}")

        for page_number, page in enumerate(pdf):

            text = clean_text(page.get_text())

            if not text:
                continue

            documents.append(

                Document(

                    page_content=text,

                    metadata={

                        "source": filename,
                        "page": page_number + 1,
                        "document": filename.replace(".pdf", "")

                    }

                )

            )

        pdf.close()

    print(f"Loaded {len(documents)} pages.\n")

    return documents


# ==========================================================
# Debug Only
# ==========================================================

if __name__ == "__main__":

    docs = load_documents()

    print("=" * 70)
    print("LOADER TEST")
    print("=" * 70)
    print(f"Total Pages : {len(docs)}")

    sources = sorted(
        {
            doc.metadata["source"]
            for doc in docs
        }
    )

    print("\nSources:")

    for source in sources:
        print("✔", source)