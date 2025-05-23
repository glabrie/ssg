from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link

def text_to_textnodes(text: str):
    node_list = [TextNode(text, TextType.TEXT, None)]
    result = (
        split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_image(split_nodes_link(node_list)), "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)
        )
    return result
#    node_list = [TextNode(text, TextType.TEXT, None)]
#    print("Initial:", node_list)
#    
#    after_links = split_nodes_link(node_list)
#    print("After links:", after_links)
#    
#    after_images = split_nodes_image(after_links)
#    print("After images:", after_images)
#
#    print("Checking each node before bold split:")
#    for i, node in enumerate(after_images):
#        print(f"  Node {i}: '{node.text}' (type: {node.text_type})")
#
#    after_bold = split_nodes_delimiter(after_images, "**", TextType.BOLD)
#    print("After bold:", after_bold)
#    
#    after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
#    print("After italic:", after_italic)
#
#    after_code = split_nodes_delimiter(after_italic, "`", TextType.CODE)
#    print("after code:", after_code)
#
#    return after_code

