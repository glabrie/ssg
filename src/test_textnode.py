import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a bold test", TextType.BOLD)
        node2 = TextNode("This is a bold test", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_different_text(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        node2 = TextNode("This isn't a bold text", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_different_text_type(self):
        # Test with different text types
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_url_property(self):
        # Test with URL specified vs None
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, None)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
