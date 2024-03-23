from node import Node, TextNode
import parsing
import utils

def parseNewlineInParagraph(input: str) -> list[Node]:
    assert input[0] == "\n"
    split = input[1:].split("\n", maxsplit=1)
    beforeNewline = split[0]
    afterNewline = split[1] if len(split) == 2 else ""
    if beforeNewline.strip() == "":
        return [parsing.ParagraphNode([])] + parsing.parseMarkdown(afterNewline)
    else:
        return utils.combineParagraph(TextNode("\n"), parsing.parseMarkdown(input[1:]))

def register():
    parsing.inlineParsers[r"\n"] = parseNewlineInParagraph
