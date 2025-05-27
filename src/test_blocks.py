import unittest
from block_markdown import block_to_block_type, markdown_to_blocks, BlockType

class TestsBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_whitespace(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockType(unittest.TestCase):
    def test_block_heading(self):
        md = "## This is a heading 2 title"
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.HEADING)
        
    def test_block_code(self):
        md = """```
        This is an example of
        multiple lines of
        code
        ```"""
        blocks = block_to_block_type(md)
        self.assertEqual(blocks, BlockType.CODE)

