import html
import re

import parsing
import utils
from node import Node, TextNode

class InlineMathNode(Node):
    tex: str
    def __init__(self, tex: str):
        self.tex = tex
    def html(self, **kargs):
        return f'<span class="inline-math">${html.escape(self.tex)}$</span>'
    def __repr__(self) -> str:
        return f"InlineMathNode(\"{self.tex}\")"

class DisplayMathNode(Node):
    tex: str
    def __init__(self, tex: str) -> None:
        self.tex = tex
    def html(self, **kargs) -> str:
        return f'<span class="display-math">$${html.escape(self.tex)}$$</span>'
    def __repr__(self) -> str:
        return f"DisplayMathNode(\"{self.tex}\")"

def parseInlineMath(input: str) -> list[Node]:
    assert input[0] == "$"
    match = re.match(r"\$.*?(\$|\n)", input)
    if match == None:
        print(f"Warning: could not find matching $ near \"{input[:15]}\"; proceeding without treating as inline math")
        return [ParagraphNode([TextNode(input)])]
    if match.group(0) == "\n":
        print(f"Warning: could not find matching $ on the same line near \"{input[:15]}\"; proceeding without treating as inline math")
        return utils.combineParagraph(
                TextNode(input[:match.end(1)]),
                parsing.parseParagraph(afterMatch[match.end(1):])
                )

    return utils.combineParagraph(
            InlineMathNode(input[1:match.start(1)]),
            parsing.parseParagraph(input[match.end(1):])
            )

def parseDisplayMath(input: str) -> list[Node]:
    assert input[:2] == "$$"
    split = input[2:].split("$$", maxsplit=1)
    if len(split) == 1:
        print(f"Warning: could not find matching $$ near \"{input[:15]}\"; proceeding by treating everything afterwards as display math")
        return [parsing.ParagraphNode([DisplayMathNode(input[2:])])]

    return utils.combineParagraph(
            DisplayMathNode(split[0]),
            parsing.parseParagraph(split[1])
            )

def parseDollarSign(input: str) -> list[Node]:
    if input[:2] == "$$": return parseDisplayMath(input)
    if input[0] == "$": return parseInlineMath(input)
    assert False

def register():
    parsing.inlineParsers[r"(?<!\\)\${1,2}"] = parseDollarSign
