from enum import Enum

class TextNode(text, text_type, url=none):
    self_text = text
    self_text_type = text_type
    self_url = url

    def __eq__(self, other):
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)
    def __repr__(text, text_type, url=none):
        return f"TextNode({text}, {text_type.value}, {url}")
