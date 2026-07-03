import os
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from rag.retriever import search_documents
from rag.ranker import rank_documents
from rag.context_builder import build_context
from rag.response_formatter import format_response

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

# ============================================================
# Gemini Model
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """
You are LawIntel.

You are an AI Legal Learning Assistant.

Rules:

1. Answer ONLY using the retrieved legal context.
2. Never make up legal information.
3. If the answer is unavailable, reply exactly:
   "I couldn't find this information in the uploaded legal documents."
4. Explain in simple language.
5. Mention the relevant law whenever available.
6. Mention the Article or Section whenever available.
7. Quote the legal provision if available.
8. Mention the source document.

Return your response in Markdown using EXACTLY this format.

# ⚖️ Legal Answer

Provide a clear legal explanation.

---

# 📝 AI Study Notes

## Definition

Explain in simple words.

## Key Points

- Point 1
- Point 2
- Point 3

## Important for Exams

Explain why this topic is important.

## Keywords

- Keyword 1
- Keyword 2
- Keyword 3

---

# ❓ Practice MCQs

### Question 1

A)

B)

C)

D)

**Answer:**

### Question 2

A)

B)

C)

D)

**Answer:**

Generate exactly TWO MCQs.
"""

# ============================================================
# Query Preprocessing
# ============================================================


def preprocess_query(question: str) -> str:
    question = question.lower()

    question = re.sub(r"\bart\b\.?", "article", question)
    question = re.sub(r"[^\w\s]", " ", question)
    question = re.sub(r"\s+", " ", question)

    return question.strip()


# ============================================================
# Ask Question
# ============================================================

def ask_question(question, mode="search"):
    print("MODE =", mode)

    # ----------------------------------
    # Clean Query
    # ----------------------------------

    question = preprocess_query(question)

    # ----------------------------------
    # Retrieve Documents
    # ----------------------------------

    docs = search_documents(question)

    # ----------------------------------
    # Rank Documents
    # ----------------------------------

    docs = rank_documents(question, docs)

    # ----------------------------------
    # Build Context
    # ----------------------------------

    context = build_context(docs)

    # ----------------------------------
    # Debug
    # ----------------------------------

    print("\n" + "=" * 80)
    print("RETRIEVED DOCUMENTS")
    print("=" * 80)

    for i, doc in enumerate(docs):

        print(f"\nDocument {i + 1}")
        print("Metadata:", doc.metadata)
        print("-" * 60)
        print(doc.page_content[:400])
        print("-" * 60)

    # ----------------------------------
    # Prompt
    # ----------------------------------

    if mode == "summary":
       print("USING SUMMARY PROMPT")

       prompt = f"""
You are LawIntel.

You are an AI Legal Learning Assistant.

Your task is to create a concise study summary from the retrieved legal context.

If the user asks a broad topic such as:

- Constitution
- IPC
- BNS
- CrPC
- Evidence Act
- Fundamental Rights

then summarize the retrieved legal context in simple language.

If the user asks about a specific Article or Section but it is NOT present in the retrieved context, then reply:

"I couldn't find this specific Article or Section in the retrieved legal documents."

Do not invent legal facts.
Use only the retrieved context."""

    else:
               print("USING SEARCH PROMPT")
               prompt = f"""
{SYSTEM_PROMPT}

LEGAL CONTEXT

{context}

USER QUESTION

{question}

Return your response in Markdown using EXACTLY this structure.

# ⚖️ Legal Answer

Give a clear legal answer.

---

# 📝 AI Study Notes

## Definition

Explain in simple words.

## Key Points

- Point 1
- Point 2
- Point 3

## Important for Exams

Mention why it is important.

## Keywords

- keyword
- keyword
- keyword

---

# ❓ Practice MCQs

### Question 1

A)

B)

C)

D)

**Answer:**

### Question 2

A)

B)

C)

D)

**Answer:**

Generate exactly TWO MCQs.
"""   
    # ----------------------------------
    # Gemini Response
    # ----------------------------------

    response = llm.invoke(prompt)

    print("\n" + "=" * 80)
    print("GEMINI RESPONSE")
    print("=" * 80)
    print(response.content)
    print("=" * 80)

    formatted_answer = format_response(response.content)

    return formatted_answer, docs
