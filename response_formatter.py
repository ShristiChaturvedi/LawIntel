import re


def format_response(answer: str):

    # Remove extra blank lines
    answer = re.sub(r"\n{3,}", "\n\n", answer)

    # Replace headings with emojis
    answer = answer.replace("Law:", "⚖️ **Law:**")
    answer = answer.replace("Article/Section:", "📌 **Article / Section:**")
    answer = answer.replace("Legal Provision:", "📖 **Legal Provision:**")
    answer = answer.replace("Explanation:", "💡 **Explanation:**")
    answer = answer.replace("Source:", "📚 **Source:**")

    return answer.strip()