from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from langchain_core.documents import Document

BASE_URL = "https://www.constitutionofindia.net/articles/article-{}"


def extract_article(article_number):

    url = BASE_URL.format(article_number)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url)

        page.wait_for_timeout(3000)

        html = page.content()

        browser.close()

    soup = BeautifulSoup(html, "lxml")

    # -----------------------
    # Part
    # -----------------------

    part = "Unknown"

    part_div = soup.find("div", class_="md:col-span-3")

    if part_div:

        text = part_div.get_text(" ", strip=True)

        if "Part" in text:
            part = text.split("Article")[0].strip()

    # -----------------------
    # Title
    # -----------------------

    title = soup.title.text.split("-")[0].strip()

    # -----------------------
    # Constitution Content
    # -----------------------

    content = ""

    blocks = soup.find_all(
        "div",
        class_="article-detail__content__sub-block"
    )

    for block in blocks:

        text = block.get_text("\n", strip=True)

        if "Constitution of India 1950" in text:
            content = text
            break

    return Document(
        page_content=content,
        metadata={
            "law": "Constitution",
            "part": part,
            "article": str(article_number),
            "title": title,
            "source": url,
        },
    )