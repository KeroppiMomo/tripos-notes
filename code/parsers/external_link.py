import re

import parsing
import utils
from node import Node, TextNode

class ExternalLinkNode(Node):
    content: list[Node]
    href: str
    def __init__(self, href: str, content: list[Node]):
        self.href = href
        self.content = content
    def html(self, **kargs):
        return f'<a href="{self.href}">{utils.list2html(self.content, **kargs)}</a>'
    def __repr__(self) -> str:
        return f'ExternalLinkNode("{self.href}", {self.content})'

# Thanks lol
# https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
URL_REGEX = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

MARKDOWN_LINK_REGEX = r"\[([^\]]*)\]\(([^)]*)\)"

def parsePlainURL(input: str) -> list[Node]:
    match = re.match(URL_REGEX, input)
    assert match is not None
    url = match.group(0)
    node = ExternalLinkNode(url, [TextNode(url)])
    return utils.combineParagraph(node, parsing.parseParagraph(input[match.end():]))

def parseMarkdownLink(input: str) -> list[Node]:
    match = re.match(MARKDOWN_LINK_REGEX, input)
    assert match is not None
    url = match.group(2)
    content = parsing.parseParagraph(match.group(1))
    node = ExternalLinkNode(url, content[0].content)
    return utils.combineParagraph(node, parsing.parseParagraph(input[match.end():]))

def register():
    # Disabling this since it is ruining iframe tags
    # parsing.inlineParsers[URL_REGEX] = parsePlainURL
    parsing.inlineParsers[MARKDOWN_LINK_REGEX] = parseMarkdownLink
