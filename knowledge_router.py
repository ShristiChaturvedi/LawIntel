import re


def detect_domain(question):

    question = question.lower()

    # Constitution
    if re.search(r"\b(article|constitution|fundamental rights|directive principles|dpsp|preamble)\b", question):
        return "constitution"

    # IPC / BNS
    if re.search(r"\b(section|ipc|indian penal code|bns|bharatiya nyaya sanhita|crime|punishment|murder|theft)\b", question):
        return "ipc"

    # CPC
    if re.search(r"\b(cpc|civil procedure|order|rule|plaint|decree|civil suit)\b", question):
        return "cpc"

    # Evidence
    if re.search(r"\b(evidence|bsa|bharatiya sakshya adhiniyam|proof|witness|admissible)\b", question):
        return "evidence"

    return "general"