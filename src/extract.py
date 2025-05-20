import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    extract = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return extract

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    extract = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return extract
