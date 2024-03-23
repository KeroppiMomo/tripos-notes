import re

from node import Node
import parsing

def parseComment(input: str) -> list[Node]:
    assert input.startswith("%%")
    match = re.search(r"(?<!\\)%%", input[2:])
    if match is None:
        return []
    return parsing.parseParagraph(input[2+match.end(0):])

def register():
    parsing.inlineParsers[r"(?<!\\)%%"] = parseComment
