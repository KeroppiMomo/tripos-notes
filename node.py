class Node:
    def __init__(self) -> None:
        pass
    def html(self, **kargs) -> str:
        raise NotImplemented()

class TextNode(Node):
    text: str
    def __init__(self, text: str) -> None:
        self.text = text
    def html(self, **kargs) -> str:
        return self.text
    def __repr__(self) -> str:
        return f"TextNode(\"{self.text}\")"

