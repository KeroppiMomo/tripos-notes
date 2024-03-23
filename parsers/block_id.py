import re

from node import Node
import parsing
import utils

class BlockIDNode(Node):
    id: str
    
    def __init__(self, id: str):
        self.id = id
    def html(self, **kargs):
        print("Warning: BlockIDNode not consumed before getting HTML")
        return ""
    def __repr__(self) -> str:
        return f'BlockIDNode("{id}")'

REGEX = r"(?:^|\s)\^([A-Za-z0-9\-]+)(?:$|\n)"
def parseBlockID(input):
    match = re.match(REGEX, input)
    assert match is not None
    id = match.group(1)
    node = BlockIDNode(id)
    return [node] + parsing.parseMarkdown(input[match.end(0):])

def register():
    parsing.inlineParsers[REGEX] = parseBlockID
