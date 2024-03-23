from typing import Optional
import re
from enum import Enum

from node import Node, TextNode
from parsers.block_id import BlockIDNode
import utils
import parsing

class ColumnAlignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class TableNode(Node):
    # cells[row][column] is a list of nodes
    id: Optional[str]
    cells: list[list[list[Node]]]
    columnAlignment: list[ColumnAlignment]
    def __init__(self, cells: list[list[list[Node]]], columnAlignment: list[ColumnAlignment], id: Optional[str] = None):
        self.cells = cells
        self.ColumnAlignment = columnAlignment
        self.id = id
    
    def rowHTML(self, rowIndex: int, **kargs):
        cellTag = "th" if rowIndex == 0 else "td"
        alignmentClasses = {
            ColumnAlignment.LEFT: "table-cell-left",
            ColumnAlignment.CENTER: "table-cell-center",
            ColumnAlignment.RIGHT: "table-cell-right",
        }
        body = "\n".join([
            f'<{cellTag} class="{alignmentClasses[self.columnAlignment[i]]}">{utils.list2html(self.cells[rowIndex][i])}</{cellTag}>'
            for i in range(len(self.cells[rowIndex]))
        ])
        return f'<tr>\n{utils.indent(body)}\n</tr>'

    def html(self, **kargs):
        body = "\n".join([self.rowHTML(i, **kargs) for i in range(len(self.cells))])
        id_attribute = f' id="{self.id}"' if self.id is not None else ""
        result = f'<table{id_attribute}>\n{utils.indent(body)}\n</table>\n'
        return utils.wrapForBlockID(self.id, result)
    def __repr__(self) -> str:
        return f'TableNode({self.columnAlignment}, {self.cells})'

def headerSegmentAlignment(segment: str) -> ColumnAlignment:
    segment = segment.strip()
    start = segment.startswith(":")
    end = segment.endswith(":")
    if start and end: return ColumnAlignment.CENTER
    if end: return ColumnAlignment.RIGHT
    if start: return ColumnAlignment.LEFT
    return ColumnAlignment.LEFT

def rowTextToCells(row: str) -> list[list[Node]]:
    split = re.split(r"(?<!\\)\|", row)
    return [parsing.parseParagraph(text) for text in split]

def parseTable(input: str) -> list[Node]:
    def removePipesAtEnds(text: str) -> str:
        text = text.strip()
        if text.startswith("|"):
            text = text[1:]
        if text.endswith("|"):
            text = text[:-1]
        return text


    node = TableNode([], [])

    lineSplit1 = input.split("\n", maxsplit=1)
    topRowText = removePipesAtEnds(lineSplit1[0])
    lineSplit2 = lineSplit1[1].split("\n", maxsplit=1)
    headerRowText = removePipesAtEnds(lineSplit2[0])
    node.columnAlignment = [headerSegmentAlignment(segment) for segment in headerRowText.split("|")]
    colNumber = len(node.columnAlignment)

    node.cells.append(rowTextToCells(topRowText)[:colNumber])
    remainingText = lineSplit2[1] if len(lineSplit2) > 1 else ""
    while True:
        split = remainingText.split("\n", maxsplit=1)
        before = split[0]
        remainingText = split[1] if len(split) > 1 else ""
        if before.strip() == "":
            break

        rowCells = rowTextToCells(before)[:colNumber]
        if len(rowCells) < colNumber:
            rowCells += [[]] * (colNumber - len(rowCells))
        node.cells.append(rowCells)
    remaining = parsing.parseMarkdown(remainingText)
    if len(remaining) > 0 and isinstance(remaining[0], BlockIDNode):
        node.id = remaining[0].id
        remaining = remaining[1:]
    return [node] + remaining

def register():
    parsing.lineStartParsers[r".*[^\\]\|.*\n[:\ \-]+\|[:|\ \t\-]+(\n|$)"] = parseTable
