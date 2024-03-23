from node import Node
import parsing
import utils

class HeadingNode(Node):
    content: list[Node]
    level: int
    def __init__(self, content: list[Node], level: int):
        self.content = content
        self.level = level
    def html(self, **kargs) -> str:
        return f"\n<h{self.level}>{utils.list2html(self.content, **kargs)}</h{self.level}>\n\n"
    def __repr__(self) -> str:
        return f"HeadingNode({self.content}, {self.level})"

def parseHeading(input: str) -> list[Node]:
    level = 0
    for char in input:
        if char == "#": level += 1
        else: break

    input = input[level:].lstrip()
    split = input.split("\n", 1)
    node = HeadingNode(parsing.parseParagraph(split[0])[0].content, level)
    return [node] + (parsing.parseMarkdown(split[1]) if len(split) > 1 else [])

def register():
    parsing.lineStartParsers[r"#+ "] = parseHeading
