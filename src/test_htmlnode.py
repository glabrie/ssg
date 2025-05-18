import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_href(self):
        node = HTMLNode(props={"href": "https://bootdev.com"})
        self.assertEqual(node.props_to_html(), ' href="https://bootdev.com"')
    
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(props={"href": "https://bootdev.com", "target": "_blank"})
        # Note: dictionary iteration order is not guaranteed, so we need to check in a way that handles any order
        result = node.props_to_html()
        self.assertIn(' href="https://bootdev.com"', result)
        self.assertIn(' target="_blank"', result)
    
    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_LeafNodeP(self):
        node = LeafNode("p", "Hello, Florence!")
        self.assertEqual(node.to_html(), "<p>Hello, Florence!</p>")

    def test_LeafNodeA(self):
        node = LeafNode("b", "Hello, Florence!")
        self.assertEqual(node.to_html(), "<b>Hello, Florence!</b>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
if __name__ == "__main__":
    _ = unittest.main()
