from typing import Optional

from node import Node, TextNode
import re

def indent(text: str, levels: int=1) -> str:
    return "\n".join(
        map(
            lambda line: (" "*4) * levels + line,
            text.split("\n")
        ))
def unindent(text: str, levels: int=1) -> str:
    # Each indent level is either a tab or at most 4 spaces
    regex = r"(\t|\ {0,4}){" + str(levels) + "}"
    return "\n".join(
        map(
            lambda line: line[
                re.match(regex, line).end(0):
            ],
            text.split("\n")
        ))

def list2html(nodes: list[Node], **kargs: dict) -> str:
    return "".join(map(lambda node: node.html(**kargs), nodes))

def regexOneOf(exprs: list[str]) -> str:
    return "|".join(map(lambda regex: f"({regex})", exprs))

def combineParagraph(node: Node, followingNodes: list[Node]) -> list[Node]:
    from parsing import ParagraphNode
    from parsers.block_id import BlockIDNode

    if len(followingNodes) > 0:
        nextNode = followingNodes[0]
        if isinstance(nextNode, ParagraphNode):
            nextNode.content.insert(0, node)
            return followingNodes
        if isinstance(nextNode, BlockIDNode):
            if isinstance(node, TextNode) and node.text.strip() == "":
                return followingNodes
            else:
                return [ParagraphNode([node], id=nextNode.id)] + followingNodes[1:]
    return [ParagraphNode([node])] + followingNodes

def wrapForBlockID(id: Optional[str], html: str):
    if id is None:
        return html
    return f"<!-- BEGIN BLOCK ID {id} -->\n{html}\n<!-- END BLOCK ID {id} -->\n"
