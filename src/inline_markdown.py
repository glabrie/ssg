import re
from textnode import TextNode, TextType

def text_to_textnodes(text: str):
    node_list = [TextNode(text, TextType.TEXT, None)]
    result = split_nodes_delimiter(
    split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_image(
                split_nodes_link(node_list)
            ),
            "**", TextType.BOLD
        ),
        "_", TextType.ITALIC
    ),
    "`", TextType.CODE
)
    return result


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list: list[TextNode] = []
    if delimiter not in ["`", "**", "_"]:
        raise Exception("No delimiter provided")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception("Unmatched delimiter in text: " + node.text)
            for i, split_node in enumerate(split_nodes):
                if i % 2 == 0:
                    new_list.append(TextNode(split_node, TextType.TEXT))
                else:
                    new_list.append(TextNode(split_node, text_type))
    return new_list

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        
        extracted_images = extract_markdown_images(node.text)

        if not extracted_images:
            new_list.append(node)
            continue

        leftover = node.text
        for alt_text, url in extracted_images:
            delimiter = f"![{alt_text}]({url})"
            remainder = leftover.split(delimiter, maxsplit=1)
            if remainder[0] != "":
                new_list.append(TextNode(remainder[0], TextType.TEXT))
            new_list.append(TextNode(alt_text, TextType.IMAGE, url))
            leftover = remainder[1]
        if leftover != "":
            new_list.append(TextNode(leftover, TextType.TEXT))
    return new_list

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        extracted_link = extract_markdown_links(node.text)

        if not extracted_link:
            new_list.append(node)
            continue

        leftover = node.text
        for alt_text, url in extracted_link:
            delimiter = f"[{alt_text}]({url})"
            remainder = leftover.split(delimiter, maxsplit=1)
            if remainder[0] != "":
                new_list.append(TextNode(remainder[0], TextType.TEXT))
            new_list.append(TextNode(alt_text, TextType.LINK, url))
            leftover = remainder[1]
        if leftover != "":
            new_list.append(TextNode(leftover, TextType.TEXT))
    return new_list

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    extract = re.findall(r"!\[([^[\]]*?)\]\(([^()]*?)\)", text)
    return extract

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    extract = re.findall(r"(?<!!)\[([^[\]]*?)\]\(([^()]*?)\)", text)
    return extract
