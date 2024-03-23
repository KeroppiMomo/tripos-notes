import re

from node import Node
import parsing
import utils

class HorizontalRuleNode(Node):
    def __init__(self):
        pass
    def html(self, **kargs) -> str:
        return "<hr>\n"
    def __repr__(self) -> str:
        return f"HorizontalRuleNode()"

REGEX = r"([\ \t]*\*){3,}[\ \t]*\n|([\ \t]*-){3,}[\ \t]*\n|([\ \t]*_){3,}[\ \t]*\n"
def parseHorizontalRule(input: str) -> list[Node]:
    match = re.match(REGEX, input)
    assert match is not None
    return [HorizontalRuleNode()] + parsing.parseMarkdown(input[match.end(0):])

def register():
    parsing.lineStartParsers[REGEX] = parseHorizontalRule
