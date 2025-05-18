from typing import override

class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list["HTMLNode"] = children if children is not None else []
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        raise NotImplementedError("If you are seeing this, override it")

    def props_to_html(self):
        return "" if self.props is None else "".join(f' {key}="{value}"' for key, value in self.props.items())

    @override
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    @override
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag: str | None, children: list["HTMLNode"], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag detected")
        if not self.children:
            raise ValueError("No children detected")
        else:
            return f"<{self.tag}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
