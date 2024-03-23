import re

from node import Node, TextNode
import parsing
import utils

class FormattingNode(Node):
    delimitor: str
    content: list[Node]
    def __init__(self, content: list[Node], delimitor: str):
        self.delimitor = delimitor
        self.content = content
    def html(self, **kargs) -> str:
        tag = {
            "**": "strong",
            "__": "strong",
            "*": "em",
            "_": "em",
            "==": "mark",
        }[self.delimitor]
        return f"<{tag}>{utils.list2html(self.content, **kargs)}</{tag}>"
    def __repr__(self) -> str:
        return f"FormattingNode(\"{self.delimitor}\", {self.content})"

def parseFormatting(input: str) -> list[Node]:
    # TODO: bad implementation, i'm lazy
    delimitor = "**" if input[:2] == "**" \
        else "*" if input[0] == "*" \
        else "__" if input[:2] == "__" \
        else "_" if input[0] == "_" \
        else "==" if input[:2] == "==" else None
    afterDelimitor = input[len(delimitor):]
    match = re.search(r"\n|" + delimitor.replace("*", "\\*"), afterDelimitor)
    if match is None or match.group(0) == "\n":
        return utils.combineParagraph(TextNode(delimitor), parsing.parseParagraph(afterDelimitor))
    else:
        node = FormattingNode(parsing.parseParagraph(afterDelimitor[:match.start(0)])[0].content, delimitor)
        return utils.combineParagraph(node, parsing.parseParagraph(afterDelimitor[match.end(0):]))

def register():
    parsing.inlineParsers[r"(?<!\\)==|\*{1,2}|_{1,2}"] = parseFormatting
