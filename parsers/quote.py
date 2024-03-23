from typing import Optional
import re

from node import Node, TextNode
from parsers.block_id import BlockIDNode
import utils
import parsing

class QuoteNode(Node):
    id: Optional[str]
    content: list[Node]
    
    def __init__(self, content: list[Node], id: Optional[str] = None):
        self.content = content
        self.id = id
    def html(self, **kargs):
        id_attribute = f' id="^{self.id}"' if self.id is not None else ""
        result = f'<blockquote{id_attribute}>\n{utils.indent(utils.list2html(self.content))}\n</blockquote>\n'
        return utils.wrapForBlockID(self.id, result)
    def __repr__(self) -> str:
        return f'QuoteNode(id={self.id}, {self.content})'

def parseQuote(input: str) -> list[Node]:
    emptyLineMatch = re.search(r"\n[\ \t]*\n", input)
    beforeMatch = input[:emptyLineMatch.start()]
    afterMatch = input[emptyLineMatch.end():]

    removedAngle = "\n".join([
        line[2:] if line.startswith("> ") else line
        for line in beforeMatch.split("\n")
    ])
    content = parsing.parseMarkdown(removedAngle)
    node = QuoteNode(content)
    after = parsing.parseMarkdown(afterMatch)

    if len(after) > 0 and isinstance(after[0], BlockIDNode):
        node.id = after[0].id
        after = after[1:]
    return [node] + after

def register():
    parsing.lineStartParsers[r"> "] = parseQuote
