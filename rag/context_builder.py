def build_context(docs):

    context = ""

    for doc in docs:

        meta = doc.metadata

        context += f"""
====================================================

Law: {meta.get('law', 'Unknown')}

Title: {meta.get('title', 'Unknown')}

Article: {meta.get('article', 'N/A')}

Section: {meta.get('section', 'N/A')}

Part: {meta.get('part', 'N/A')}

Source: {meta.get('source', 'Unknown')}

Content:

{doc.page_content}

"""

    return context
