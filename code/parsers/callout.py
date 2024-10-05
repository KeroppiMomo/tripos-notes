from typing import Optional
import re

from node import Node, TextNode
from parsers.block_id import BlockIDNode
import utils
import parsing

# Regex explanation:
# Literal > [!                              > \[
# followed by one or more characters        (.+)            capture group 1
# then ]                                    \]
# then either                               (?:...|...)     non-capturing group
#       zero or more spaces or tabs         [\ \t]*
# or
#       one or more spaces or tabs          [\ \t]+
#       followed by one of more characters  (.+)            capture group 2
# then newline                              \n
REGEX = r"> \[!(.+)\](?:[\ \t]*|[\ \t]+(.+))\n"

class CalloutNode(Node):
    id: Optional[str]

    typeId: str
    title: str
    content: list[Node]
    
    def __init__(self, typeId: str, title: str, content: list[Node], id: Optional[str] = None):
        self.typeId = typeId
        self.title = title
        self.content = content
        self.id = id
    def html(self, **kargs):
        id_attribute = f' id="^{self.id}"' if self.id is not None else ""
        result = f'''<div{id_attribute} class="markdown-callout" data-callout="{self.typeId}">
    <div class="markdown-callout-title">
        <i data-lucide="file-text"></i>
        <div class="markdown-callout-title-inner">{self.title}</div>
    </div>
    <div class="markdown-callout-content">
{utils.indent(utils.list2html(self.content), 2)}
    </div>
</div>'''
        return utils.wrapForBlockID(self.id, result)
    def __repr__(self) -> str:
        return f'CalloutNode(id={self.id}, {self.typeId}, {self.title}, {self.content})'

def parseCallout(input: str) -> list[Node]:
    emptyLineMatch = re.search(r"\n[\ \t]*\n", input)
    beforeMatch = input[:emptyLineMatch.start()] if emptyLineMatch is not None else input
    afterMatch = input[emptyLineMatch.end():] if emptyLineMatch is not None else ""

    firstLineMatch = re.match(REGEX, beforeMatch)
    assert firstLineMatch is not None, "Should have checked REGEX matches"
    betweenMatch = beforeMatch[firstLineMatch.end():]
    typeId = firstLineMatch.group(1)
    assert typeId is not None, "REGEX match should capture at least one group"
    title = firstLineMatch.group(2)
    if title is None:
        title = typeId[0].upper() + typeId[1:]

    removedAngle = "\n".join([
        line[2:] if line.startswith("> ") else line
        for line in betweenMatch.split("\n")
    ])
    content = parsing.parseMarkdown(removedAngle)
    node = CalloutNode(typeId, title, content)
    after = parsing.parseMarkdown(afterMatch)

    if len(after) > 0 and isinstance(after[0], BlockIDNode):
        node.id = after[0].id
        after = after[1:]
    return [node] + after

def register():
    parsing.lineStartParsers[REGEX] = parseCallout
