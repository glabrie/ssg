from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links

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
            if len(split_nodes) == 1:
                raise Exception("Unmatched delimiter in text: " + node.text)
            for i, split_node in enumerate(split_nodes):
                if i % 2 == 0:
                    new_list.append(TextNode(split_node, TextType.TEXT))
                else:
                    new_list.append(TextNode(split_node, text_type))
    return new_list

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        
        extracted = extract_markdown_images(node.text)

        if not extracted:
            new_list.append(node)
        
        leftover = node.text
        for alt.text, url in extracted:

