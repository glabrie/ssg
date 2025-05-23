import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from extract import extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitDelimiterBold(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a **sample** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        should_be = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("sample", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
                ]
        self.assertEqual(result, should_be)

class TestSplitDelimiterCode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a `sample` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        should_be = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("sample", TextType.CODE),
            TextNode(" text", TextType.TEXT)
                ]
        self.assertEqual(result, should_be)

class TestSplitDelimiterItalic(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a _sample_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        should_be = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("sample", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
                ]
        self.assertEqual(result, should_be)

class TestSplitNoType(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a sample text", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            _ = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("Unmatched delimiter in text: This is a sample text", str(context.exception))

class Extract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)

class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is a text with a [link](https://boot.dev) and another [link](https://archlinux.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://archlinux.org"),
            ],
            new_nodes,
        )

    def test_split_no_image(self):
        node = TextNode(
            "This is text with no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with no image", TextType.TEXT, None)], new_nodes)

    def test_split_no_link(self):
        node = TextNode(
            "This is text with no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is text with no link", TextType.TEXT, None)], new_nodes)

    def test_split_out_of_order(self):
        node = TextNode(
            "[link](https://boot.dev) and another [link](https://archlinux.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://archlinux.org"),
            ],
            new_nodes,
        )

    def test_split_out_of_order2(self):
        node = TextNode(
            "[link](https://boot.dev)[link](https://archlinux.org) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("link", TextType.LINK, "https://archlinux.org"),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_nothing_to_split(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("", TextType.TEXT, None)], new_nodes)

    def test_overload_links(self):
        node = TextNode(
            "This is a text with a [![image](https://animage.com](https://boot.dev) and another [link](https://archlinux.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a [![image](https://animage.com](https://boot.dev) and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://archlinux.org"),
            ],
            new_nodes,
        )

    def test_overload_images(self):
        node = TextNode(
            "This is an ![[image](https://animage.com)](https://animage.com) and another ![image](https://animage.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an ![[image](https://animage.com)](https://animage.com) and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://animage.com"),
            ],
            new_nodes,
        )
