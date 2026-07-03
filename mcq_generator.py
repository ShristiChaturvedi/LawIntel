import os
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from rag.retriever import search_documents
from rag.ranker import rank_documents
from rag.context_builder import build_context

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# ==========================================================
# Format MCQs
# ==========================================================

def format_mcqs(text):

    # Put options on separate lines
    text = re.sub(r"\s(A[\.\)])", r"\n\1", text)
    text = re.sub(r"\s(B[\.\)])", r"\n\1", text)
    text = re.sub(r"\s(C[\.\)])", r"\n\1", text)
    text = re.sub(r"\s(D[\.\)])", r"\n\1", text)

    # Beautify answer heading
    text = text.replace("Answer:", "✅ Correct Answer:")

    # Beautify explanation heading
    text = text.replace("Explanation:", "📝 Explanation:")

    return text


# ==========================================================
# Generate MCQs
# ==========================================================

def generate_mcqs(question):

    docs = search_documents(question)

    docs = rank_documents(question, docs)

    context = build_context(docs)

    prompt = f"""
You are LawIntel.

You are an expert Constitutional and Criminal Law educator.

Use ONLY the legal context below.

====================================================
LEGAL CONTEXT
====================================================

{context}

====================================================
USER REQUEST
====================================================

{question}

Generate EXACTLY FIVE exam-style MCQs.

Rules:

1. Use ONLY the legal context.
2. Do NOT invent facts.
3. Every question must have exactly four options.
4. Every option MUST be on a separate line.
5. Mention the correct answer.
6. Give a one or two sentence explanation.
7. Keep questions suitable for Judiciary, UPSC, CLAT and Law Exams.

Return EXACTLY in this format:

# 📘 Constitutional Law Practice Test

## Question 1

<Question>

A. Option

B. Option

C. Option

D. Option

Answer: A

Explanation:
<1-2 sentence explanation>

--------------------------------------

Repeat until Question 5.

Do not use markdown tables.

Do not put options on one line.

If the legal context is insufficient, reply ONLY:

I couldn't generate MCQs from the retrieved legal documents.
"""

    response = llm.invoke(prompt)

    formatted = format_mcqs(response.content)

    return formatted, docs