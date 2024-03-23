from typing import Optional
from pathlib import Path
import re

from node import Node, TextNode
import parsing
import utils
import file_manager

import config

class WikilinkNode(Node):
    fullPath: Path
    fragment: str
    displayContent: list[Node]
    def __init__(self, fullPath: Path, fragment: str, displayContent: list[Node]):
        self.fullPath = fullPath
        self.fragment = fragment
        self.displayContent = displayContent
    def html(self, **kargs: dict) -> str:
        absolutePath = "/" / (file_manager.vaultToOutputPath(self.fullPath, bareMarkdown=False).relative_to(file_manager.OUTPUT_ROOT_PATH))
        url = str(absolutePath) + ("#" + self.fragment if self.fragment is not None else "")
        return f'<a href="{url}">{utils.list2html(self.displayContent, **kargs)}</a>'
    def __repr__(self) -> str:
        return f'WikilinkNode("{self.fullPath}", "{self.fragment}", {self.displayContent})'

class MarkdownEmbedNode(Node):
    fullPath: Path
    fragment: str
    def __init__(self, fullPath: Path, fragment: str) -> None:
        self.fullPath = fullPath
        self.fragment = fragment

    def extractingTargetedPortion(html: str, fragment: str) -> str:
        if fragment.startswith("^"):
            id = fragment[1:]
            split1 = html.split(f"<!-- BEGIN BLOCK ID {id} -->\n", maxsplit=1)
            if len(split1) == 1:
                print(f'Error: could not find block ID "{id}"; proceeding by ignoring the fragment')
                return html
            split2 = split1[1].split(f"<!-- END BLOCK ID {id} -->\n")
            if len(split2) == 1:
                print(f'Error: could not find block ID "{id}"; proceeding by ignoring the fragment')
                return html
            html = split2[0].strip()
            if html.startswith("<li"):
                return f'<ul>{html}</ul>'
            else:
                return html
        else:
            print("Error: only currently support block ID as embed fragment")
            return html

    def html(self, **kargs) -> str:
        absolutePath = "/" / (file_manager.vaultToOutputPath(self.fullPath, bareMarkdown=False).relative_to(file_manager.OUTPUT_ROOT_PATH))
        url = str(absolutePath) + ("#" + self.fragment if self.fragment is not None else "")
        contentHTML = file_manager.requestBareOutputAtPath(self.fullPath)
        if self.fragment is not None:
            contentHTML = MarkdownEmbedNode.extractingTargetedPortion(contentHTML, self.fragment)

        title = self.fullPath.stem
        classes = ["markdown-embed"] + config.customEmbedClasses(self.fullPath)
        return f'''<div class="{' '.join(classes)}">
    <div class="markdown-embed-title">
        {title}
        <a class="markdown-embed-open" title="Open" href="{url}">open_in_new</a>
    </div>
    <div class="markdown-embed-content">
{utils.indent(contentHTML, 2)}
    </div>
</div>'''
    def __repr__(self) -> str:
        return f'MarkdownEmbedNode("{self.fullPath}", "{self.fragment}")'

class ImageNode(Node):
    fullPath: str
    width: Optional[float]
    height: Optional[float]
    def __init__(self, fullPath: str, width: Optional[float], height: Optional[float]) -> None:
        assert not (width is None and height is not None)
        self.fullPath = fullPath
        self.width = width
        self.height = height
    def html(self, sourcePath: Path=None, **kargs) -> str:
        absolutePath = "/" / (file_manager.vaultToOutputPath(self.fullPath).relative_to(file_manager.OUTPUT_ROOT_PATH))
        width_attribute = f' width="{self.width}"' if self.width is not None else ""
        height_attribute = f' height="{self.height}"' if self.height is not None else ""
        return f'<img src="{absolutePath}"{width_attribute}{height_attribute}>'
    def __repr__(self) -> str:
        return f'ImageNode("{self.fullPath}", {self.width}, {self.height})'

def parseWikilinks(input: str) -> list[Node]:
    assert input[:2] == "[[" or input[:3] == "![["
    isEmbed = input[0] == "!"
    match = re.search(r"\]\]|\n", input)
    if match is None or match.group(0) == "\n":
        print(f"Warning: could not find matching ]] after {input[:10]}; proceeding by treating as text")
        return utils.combineParagraph(TextNode(input[:match.end(0)]), parsing.parseParagraph(input[match.end(0):]))
    afterLink = input[match.end(0):]
    linkContent = input[3 if isEmbed else 2: match.start(0)]

    strokeSplit = linkContent.split("|", maxsplit=1)
    displayText: Optional[str] = strokeSplit[1] if len(strokeSplit) == 2 else None
    fragmentSplit = strokeSplit[0].split("#", maxsplit=1)
    shortPath = fragmentSplit[0]
    fragment: Optional[str] = fragmentSplit[1] if len(fragmentSplit) == 2 else None

    if not isEmbed:
        displayContent = [TextNode(shortPath)] if displayText is None else parsing.parseParagraph(displayText)[0].content
        fullPath = file_manager.resolveToVaultPath(shortPath)
        if fullPath is None:
            print(f'Error: could not find file "{shortPath}"; showing error')
            node = TextNode(f"[[FILE NOT FOUND: {shortPath}]]")
        else:
            node = WikilinkNode(fullPath, fragment, displayContent)
    else:
        fullPath = file_manager.resolveToVaultPath(shortPath)
        if fullPath is None:
            print(f'Error: could not find file "{shortPath}"; showing error')
            node = TextNode(f"[[FILE NOT FOUND: {shortPath}]]")
        elif fullPath.suffix == ".md":
            node = getMarkdownEmbedNode(fullPath, fragment, displayText)
        elif fullPath.suffix in [".gif", ".jpg", ".jpeg", ".png", ".svg"]:
            node = getImageNode(fullPath, fragment, displayText)
        else:
            print(f'Error: unknown file extension in "{shortPath}"; showing error')
            node = TextNode(f"[[UNKNOWN FILE EXTENSION: {shortPath}]]")

    return utils.combineParagraph(node, parsing.parseParagraph(afterLink))

def getMarkdownEmbedNode(fullPath: Path, fragment: str, displayText: str):
    return MarkdownEmbedNode(fullPath, fragment)
def getImageNode(fullPath, fragment, displayText):
    width = None; height = None
    if displayText is not None:
        try:
            width_heigth_split = displayText.split("x", maxsplit=1)
            width = float(width_heigth_split[0])
            height = float(width_heigth_split[1]) if len(width_heigth_split) > 1 else None
        except:
            print(f'Warning: could not obtain width/height of an embeded image: "{displayText}"')
    return ImageNode(fullPath, width, height)

def register():
    parsing.inlineParsers[r"(?<!\\)!?\[\["] = parseWikilinks
