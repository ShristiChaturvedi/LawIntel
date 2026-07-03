from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from rag.knowledge_router import detect_domain

# ==========================================================
# Embedding Model
# ==========================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================================
# Load FAISS Vector Store
# ==========================================================

vector_db = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True
)

# ==========================================================
# Search Documents
# ==========================================================

def search_documents(question):

    domain = detect_domain(question)

    print("\n" + "=" * 80)
    print(f"Detected Domain : {domain}")
    print("=" * 80)

    # ------------------------------------------------------
    # Broad Topic Detection
    # ------------------------------------------------------

    broad_topics = {
        "constitution",
        "ipc",
        "bns",
        "crpc",
        "cpc",
        "evidence",
        "evidence act",
        "bharatiya nyaya sanhita",
        "fundamental rights",
        "directive principles"
    }

    is_broad_query = question.lower().strip() in broad_topics

    # ------------------------------------------------------
    # Retrieve Documents
    # ------------------------------------------------------

    if is_broad_query:

        docs = vector_db.max_marginal_relevance_search(
            query=question,
            k=20,
            fetch_k=60
        )

    else:

        docs = vector_db.max_marginal_relevance_search(
            query=question,
            k=10,
            fetch_k=40
        )

    # ------------------------------------------------------
    # Domain Filtering
    # ------------------------------------------------------

    filtered_docs = []

    for doc in docs:

        document = doc.metadata.get("document", "").lower()

        if domain == "constitution":

            if (
                "constitution" in document
                or "contitution" in document
            ):
                filtered_docs.append(doc)

        elif domain == "ipc":

            if (
                "ipc" in document
                or "bns" in document
            ):
                filtered_docs.append(doc)

        elif domain == "cpc":

            if "cpc" in document:
                filtered_docs.append(doc)

        elif domain == "evidence":

            if (
                "evidence" in document
                or "bsa" in document
            ):
                filtered_docs.append(doc)

        else:

            filtered_docs.append(doc)

    # ------------------------------------------------------
    # Fallback
    # ------------------------------------------------------

    if not filtered_docs:

        filtered_docs = docs

    # ------------------------------------------------------
    # Remove Duplicate Chunks
    # ------------------------------------------------------

    unique_docs = []
    seen = set()

    for doc in filtered_docs:

        text = doc.page_content.strip()

        if text not in seen:

            seen.add(text)
            unique_docs.append(doc)

    # ------------------------------------------------------
    # Debug
    # ------------------------------------------------------

    print(f"\nRetrieved {len(unique_docs)} unique documents.\n")

    for i, doc in enumerate(unique_docs[:10]):

        print(f"Document {i+1}")

        print(doc.metadata)

        print("-" * 60)

        print(doc.page_content[:250])

        print("-" * 60)

    # ------------------------------------------------------
    # Return Documents
    # ------------------------------------------------------

    if is_broad_query:

        return unique_docs[:15]

    return unique_docs[:8]