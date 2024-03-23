import importlib
from typing import Optional
import re

from node import Node, TextNode
import utils

def registerParsers() -> None:
    import config
    for module in config.PARSER_MODULE_NAMES:
        importlib.import_module(module).register()

class ParagraphNode(Node):
    content: list[Node]
    id: Optional[str]
    def __init__(self, content: list[Node], id: Optional[str] = None):
        self.content = content
        self.id = id
    def html(self, **kargs: dict) -> str:
        contentHTML = utils.list2html(self.content, **kargs).strip()
        if contentHTML == "":
            return ""

        id_attribute = f' id="^{self.id}"' if self.id is not None else ""
        result = f"<p{id_attribute}>\n{utils.indent(contentHTML)}\n</p>\n"
        return utils.wrapForBlockID(self.id, result)
    def __repr__(self) -> str:
        return f"ParagraphNode(id={self.id}, {self.content})"


inlineParsers = {}
def inlineRegex():
    return utils.regexOneOf(inlineParsers.keys())
def parseParagraph(input: str) -> list[Node]:
    match = re.search(inlineRegex(), input)
    if match == None:
        return [ParagraphNode([TextNode(input)])]

    beforeMatch = input[:match.start()]
    afterMatch = input[match.end():]
    textNode = TextNode(beforeMatch)
    for regex, parser in inlineParsers.items():
        if re.match(regex, match.group(0)):
            return utils.combineParagraph(textNode, parser(input[match.start():]))
    assert False

lineStartParsers = {}
def lineStartRegex():
    return utils.regexOneOf(lineStartParsers.keys())
def parseLineStart(input: str) -> list[Node]:
    for regex, parser in lineStartParsers.items():
        if re.match(regex, input):
            return parser(input)
    assert False

def parseMarkdown(input: str) -> list[Node]:
    if re.match(lineStartRegex(), input):
        return parseLineStart(input)
    return parseParagraph(input)
