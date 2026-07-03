import re


def rank_documents(question, docs):

    question = question.lower()

    article_match = re.search(r"article\s+(\d+[a-z]?)", question)
    section_match = re.search(r"section\s+(\d+[a-z]?)", question)

    scored_docs = []

    for doc in docs:

        score = 0

        text = doc.page_content.lower()

        # Exact article match
        if article_match:

            article = article_match.group(1)

            if doc.metadata.get("article") == article:
                score += 100

            if f"article {article}" in text:
                score += 50

        # Exact section match
        if section_match:

            section = section_match.group(1)

            if doc.metadata.get("section") == section:
                score += 100

            if f"section {section}" in text:
                score += 50

        # Slight bonus for shorter chunks
        score -= len(text) / 1000

        scored_docs.append((score, doc))

    scored_docs.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [doc for score, doc in scored_docs]
