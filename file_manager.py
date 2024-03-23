from typing import Optional
from pathlib import Path
import shutil
from unidecode import unidecode
import re

import parsing
import utils

import config

VAULT_ROOT_PATH = Path(config.VAULT_ROOT).expanduser()
assert VAULT_ROOT_PATH.exists()

OUTPUT_ROOT_PATH = Path(config.OUTPUT_ROOT).expanduser()

ENCODING = "utf-8"

class FileGraph:
    links: dict[Path, list[Path]]
    backlinks: dict[Path, list[Path]]

    def __init__(self):
        self.links = {}
        self.backlinks = {}

    def linksFrom(self, path: Path) -> list[Path]:
        if path not in self.links:
            self.links[path] = []
        return self.links[path]

    def backlinksTo(self, path: Path) -> list[Path]:
        if path not in self.backlinks:
            self.backlinks[path] = []
        return self.backlinks[path]

    def addLink(self, _from: Path, to: Path):
        self.linksFrom(_from).append(to)
        self.backlinksTo(to).append(_from)

fileGraph = FileGraph()
referenced_files: set[Path] = set()
processing_files: list[Path] = []
processed_files: set[Path] = set()

def rglobWithoutDotFiles(path: Path, pattern: str):
    glob = path.rglob(pattern)
    return list(filter(
        lambda path: all(not part.startswith(".") for part in path.parts),
        glob
    ))

# Convert shortPath that a user may specify to vault path
def resolveToVaultPath(shortPath: str, markedAsReferenced: bool=True) -> Optional[Path]:
    if Path(shortPath).suffix == "":
        shortPath = str(Path(shortPath).with_suffix(".md"))
    matches = rglobWithoutDotFiles(VAULT_ROOT_PATH, shortPath)
    if len(matches) == 0:
        matches = rglobWithoutDotFiles(VAULT_ROOT_PATH, shortPath + ".md")
        if len(matches) == 0:
            return None
    if len(matches) > 1:
        print(f'Warning: multiple candidates when resolving path "{shortPath}"; picking "{matches[0]}" instead of "{matches[1]}" and possibly others')
    fullPath = matches[0]
    
    if markedAsReferenced:
        fileGraph.addLink(processing_files[-1], fullPath)
        if fullPath not in processed_files:
            referenced_files.add(fullPath)

    return fullPath

def cleanPathForURL(path: Path) -> Path:
    suffix = path.suffix
    withoutSuffix = path.with_suffix("")
    result = Path()
    for part in withoutSuffix.parts:
        ascii = unidecode(part)
        # Unreserved character https://en.wikipedia.org/wiki/Percent-encoding
        reserved_split = re.split(r"[^A-Za-z0-9.~_\-]+", ascii)
        unreserved = "-".join(filter(lambda s: s != "", reserved_split))
        result /= unreserved
    return result.with_suffix(suffix)

def vaultToOutputPath(vaultPath: Path, bareMarkdown: bool=True) -> Path:
    override = config.outputPathOverride(vaultPath, VAULT_ROOT_PATH, OUTPUT_ROOT_PATH)
    if override is not None:
        return override

    vaultRelativePath = vaultPath.relative_to(VAULT_ROOT_PATH)
    cleanPath = cleanPathForURL(vaultRelativePath)
    if cleanPath.suffix == ".md":
        if bareMarkdown:
            return (OUTPUT_ROOT_PATH / "_bare" / cleanPath).with_suffix(".md.html")
        else:
            return (OUTPUT_ROOT_PATH / cleanPath).with_suffix(".html")
    else:
        return OUTPUT_ROOT_PATH / "media" / cleanPath

def generateBare(vaultPath: Path):
    print(f"Bare {len(processed_files)}/{len(processed_files) + len(referenced_files) + len(processing_files)}: {", ".join(map(lambda path: path.parts[-1], processing_files))}")
    outputPath = vaultToOutputPath(vaultPath)
    outputPath.parent.mkdir(parents=True, exist_ok=True)

    if vaultPath.suffix != ".md":
        shutil.copy(vaultPath, outputPath)
    else:
        markdown = vaultPath.read_text()

        parsed = parsing.parseMarkdown(markdown)
        html = utils.list2html(parsed, sourcePath=vaultPath)

        outputPath.write_text(html, encoding=ENCODING)

def generateAllBare(initialPaths: list[Path]):
    fileGraph = FileGraph()

    referenced_files.update(initialPaths)

    while len(referenced_files) > 0:
        curPath = referenced_files.pop()
        processing_files.append(curPath)
        generateBare(curPath)
        processing_files.pop()
        processed_files.add(curPath)

def requestBareOutputAtPath(vaultPath: Path) -> str:
    if vaultPath in processing_files:
        raise Error(f"Could not process output request for {vaultPath} since it is still processing (probably due to circular references)")

    if vaultPath not in processed_files:
        referenced_files.remove(vaultPath)
        processing_files.append(vaultPath)
        generateBare(vaultPath)
        processing_files.remove(vaultPath)
        processed_files.add(vaultPath)

    outputPath = vaultToOutputPath(vaultPath)
    return outputPath.read_text()

def getNavigationFileListHTML(paths: set[Path]):
    return "\n".join(
        map(
            lambda path:
            f'<li class="nav-file"><a href="{config.WEB_URL_ROOT}{vaultToOutputPath(path, bareMarkdown=False).relative_to(OUTPUT_ROOT_PATH)}">{path.stem}</a></li>',
            paths
        )
    )
def getBacklinksHTML(vaultPath: Path) -> str:
    backlinks = fileGraph.backlinksTo(vaultPath)
    if len(backlinks) == 0:
        return ""
    return f'''<h1 class="nav-heading">Backlinks</h1>
<ul>
{utils.indent(getNavigationFileListHTML(backlinks))}
</ul>'''

def getOutgoingLinksHTML(vaultPath: Path) -> str:
    links = fileGraph.linksFrom(vaultPath)
    if len(links) == 0:
        return ""
    return f'''<h1 class="nav-heading">Outgoing Links</h1>
<ul>
{utils.indent(getNavigationFileListHTML(links))}
</ul>'''

class FileTreeNode:
    isFolder: bool
    folderContents: dict[str, 'FileTreeNode']
    path: Path

    def __init__(self, isFolder: bool, folderContents: dict[str, 'FileTreeNode'], path: Path):
        self.isFolder = isFolder
        self.folderContents = folderContents
        self.path = path

def getProcessedFileTree() -> FileTreeNode:
    root = FileTreeNode(True, {}, VAULT_ROOT_PATH)
    for path in processed_files:
        relativePath = path.relative_to(VAULT_ROOT_PATH)
        parts = relativePath.parts
        curFolderTree = root
        folderPath = VAULT_ROOT_PATH
        for folder in parts[:-1]:
            contents = curFolderTree.folderContents
            folderPath = folderPath / folder
            if folder not in contents:
                contents[folder] = FileTreeNode(True, {}, folderPath)
            assert contents[folder].isFolder
            curFolderTree = contents[folder]

        file = parts[-1]
        assert file not in curFolderTree.folderContents
        curFolderTree.folderContents[file] = FileTreeNode(False, {}, path)

    return root

cachedFileTreeHTML: Optional[str] = None
def getFileTreeHTML(tree: Optional[FileTreeNode] = None) -> str:
    global cachedFileTreeHTML
    if tree is None:
        if cachedFileTreeHTML is None:
            cachedFileTreeHTML = getFileTreeHTML(getProcessedFileTree())
        return cachedFileTreeHTML

    files = []
    folders = []
    for key in tree.folderContents:
        if tree.folderContents[key].isFolder: folders.append(key)
        else: files.append(key)
    files = sorted(files)
    folders = sorted(folders)

    foldersHTML = "\n".join(
        map(
            lambda folder: f'''<li class="nav-folder">
    <a href="#" onclick="toggleNavFolder(this)">{folder}</a>
{utils.indent(getFileTreeHTML(tree.folderContents[folder]))}
</li>''',
            folders
    ))
    filesHTML = getNavigationFileListHTML(map(lambda file: tree.folderContents[file].path, files))
    
    return f'''<ul>
{utils.indent(foldersHTML)}
{utils.indent(filesHTML)}
</ul>'''

pageFormatCached: Optional[str] = None
def generateFormatted(vaultPath: Path):
    global pageFormatCached
    if pageFormatCached is None:
        pageFormatCached = Path(config.MARKDOWN_PAGE_FORMAT).read_text()

    barePath = vaultToOutputPath(vaultPath, bareMarkdown=True)
    bareHtml = barePath.read_text()

    backlinksHTML = getBacklinksHTML(vaultPath)
    outgoingLinksHTML = getOutgoingLinksHTML(vaultPath)
    fileTreeHTML = getFileTreeHTML()

    output = pageFormatCached \
        .replace("{{web_url_root}}", config.WEB_URL_ROOT) \
        .replace("{{title}}", vaultPath.stem) \
        .replace("{{backlinks}}", utils.indent(backlinksHTML, levels=2)) \
        .replace("{{outgoing_links}}", utils.indent(outgoingLinksHTML, levels=2)) \
        .replace("{{file_tree}}", utils.indent(fileTreeHTML, levels=2)) \
        .replace("{{bare_html}}", utils.indent(bareHtml, levels=3))

    outputPath = vaultToOutputPath(vaultPath, bareMarkdown=False)
    outputPath.parent.mkdir(parents=True, exist_ok=True)
    outputPath.write_text(output, encoding=ENCODING)

def generateAllFormatted():
    remainingFiles = processed_files.copy()
    while len(remainingFiles) != 0:
        path = remainingFiles.pop()
        print(f"Formatted {len(processed_files) - len(remainingFiles)}/{len(processed_files)}: {path.parts[-1]}")
        if path.suffix == ".md":
            generateFormatted(path)
