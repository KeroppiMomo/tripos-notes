from typing import Optional
import re

from node import Node, TextNode
from parsers.block_id import BlockIDNode
import utils
import parsing

class ListItemNode(Node):
    id: Optional[str]
    content: list[Node]

    def __init__(self, content: list[Node], id: Optional[str] = None) -> None:
        self.content = content
        self.id = id
    def html(self, **kargs: dict) -> str:
        body = utils.list2html(self.content, **kargs)
        if self.id is None:
            return f'<li>\n{utils.indent(body)}\n</li>'
        else:
            return f'<!-- BEGIN BLOCK ID {self.id} -->\n<li id="^{self.id}">\n{utils.indent(body)}\n</li>\n<!-- END BLOCK ID {self.id} -->\n'
    def __repr__(self) -> str:
        return f'ListItemNode(id={id}, {content})'


class ListNode(Node):
    id: Optional[str]
    items: list[ListItemNode]
    startCount: Optional[int] # None for unordered list

    def __init__(self, items: list[ListItemNode], startCount: Optional[int], id: Optional[str] = None) -> None:
        self.items = items
        self.startCount = startCount
        self.id = id
    def html(self, **kargs: dict) -> str:
#        def makeItemHTML(item: list[Node]):
#            content = utils.list2html(item, **kargs)
#            itemID: Optional[str] = None
#            for node in item:
#                if hasattr(node, "id") and node.id is not None:
#                    if itemID is not None:
#                        print(f'Warning: multiple block ID specified within one list item; proceeding by taking the last one "{node.id}" rather than "{itemID}"')
#                    itemID = node.id
#                    node.id = None

        body = utils.list2html(self.items)

        id_attribute = f' id="^{self.id}"' if self.id is not None else ""
        result = ""
        if self.startCount is None:
            result = f"<ul{id_attribute}>\n{body}\n</ul>\n"
        else:
            result = f'<ol{id_attribute} start="{self.startCount}">\n{body}\n</ol>\n'
        return utils.wrapForBlockID(self.id, result)
    def __repr__(self) -> str:
        return f'ListNode(id={self.id}, {self.startCount}, {self.items})'

def separateListItem(input) -> tuple[list[Node], list[Node]]:
    # Regex explanation: this searches for empty lines that the text following them are not indented.
    # \n            What comes after a newline...
    # (...)+        is one or more empty lines, that is...
    #     [\ \t]*   any number of tabs and spaces...
    #     \n        followed by a newline, ...
    # (?!...)       that cannot be followed by an indent, that is...
    #     \t|\ {3}  either a tab or three spaces.
    lastIndentedRegex = r"\n([\ \t]*\n)+(?!\t|\ {3})"
    match = re.search(f"\\n(?={parsing.lineStartRegex()})|{lastIndentedRegex}", input)
    if match is None:
        beforeMatch = input
        afterMatch = ""
    else:
        beforeMatch = input[:match.start(0)]
        afterMatch = input[match.end(0):]
    return (parsing.parseMarkdown(utils.unindent(beforeMatch)), parsing.parseMarkdown(afterMatch))

def listItemFromContent(content: list[Node]):
    id: Optional[str] = None
    for node in content:
        if hasattr(node, "id") and node.id is not None:
            if id is not None:
                print(f'Warning: multiple block ID specified within one list item; proceeding by taking the last one "{node.id}" rather than "{itemID}"')
            id = node.id
            node.id = None
    return ListItemNode(content, id=id)

UNORDERED_LIST_REGEX = r"[-*+] "
def parseUnorderedList(input) -> list[Node]:
    match = re.match(UNORDERED_LIST_REGEX, input)
    assert match is not None
    afterBullet = input[match.end(0):].lstrip()
    item, after = separateListItem(afterBullet)
    listItemNode = listItemFromContent(item)

    if isinstance(after[0], ListNode) and after[0].startCount is None:
        after[0].items.insert(0, listItemNode)
        return after
    else:
        id = None
        if len(after) > 0 and isinstance(after[0], BlockIDNode):
            id = after[0].id
            after.pop(0)
        return [ListNode([listItemNode], None, id=id)] + after

ORDERED_LIST_REGEX = r"(\d+)\. "
def parseOrderedList(input) -> list[Node]:
    match = re.match(ORDERED_LIST_REGEX, input)
    assert match is not None
    number = int(match.group(1))
    afterNumber = input[match.end(0):].lstrip()
    item, after = separateListItem(afterNumber)
    listItemNode = listItemFromContent(item)

    if isinstance(after[0], ListNode) and after[0].startCount is not None:
        after[0].items.insert(0, listItemNode)
        after[0].startCount = number
        return after
    else:
        id = None
        if len(after) > 0 and isinstance(after[0], BlockIDNode):
            id = after[0].id
            after.pop(0)
        return [ListNode([listItemNode], number, id=id)] + after

def register():
    parsing.lineStartParsers[UNORDERED_LIST_REGEX] = parseUnorderedList
    parsing.lineStartParsers[ORDERED_LIST_REGEX] = parseOrderedList
