from typing import Optional
from pathlib import Path

# Hello! The configuration parameters are put in increasing technicality...

# ------------------------------------------
# REQUIRED parameters

# Be honest and put the path to the root of the Obsidian vault.
# This is to resolve paths properly.
VAULT_ROOT = "~/Documents/obsidian-main/"

# Where you want to output the web pages.
# If you want to host the files, this is the root folder to set up the web server.
OUTPUT_ROOT = "../public/"

# True if the output folder should be deleted initially before any processing.
# False if you want to keep files the output folder. (But files may be overwritten)
CLEAR_OUTPUT_FOLDER = True

# Convert the following files, and recursively all files referenced.
INITIAL_FILES = ["~/Documents/obsidian-main/Lectures/Moses's Maths Notes.md"]

# Path to a HTML template file for the convertion from a markdown file.
# Include the following placeholers in the template file:
# - {{web_root_url}}    path on a web URL that corresponds to the output folder (see WEB_URL_ROOT);
# - {{title}}           title of this markdown file;
# - {{bare_html}}       main body of the markdown content;
# - {{backlinks}}       links of other markdown files pointing to this markdown file;
# - {{outgoing_links}}  links in this markdown file to other markdown files;
# - {{file_tree}}       file tree of all files processed.
MARKDOWN_PAGE_FORMAT = "./res/markdown_page_format.html"

# Path to the LaTeX preamble used for MathJax.
MATHJAX_PREAMBLE = "~/Documents/obsidian-main/preamble.sty"

# Path to the MathJax config JavaScript file.
# Include the placeholder {{preamble}} for a JavaScript escaped string of the preamble.
MATHJAX_CONFIG_FORMAT = "./res/mathjax-config-format.js"

# Path to a folder containing static resources.
# Contents in this folder will be copied to the output folder.
STATIC_FOLDER = "./res/static/"

# Path that you want the 404 page to be outputted at.
# None if you do not want the page to be generated.
PAGE_404 = "../public/404.html"

# URL path to the root of the output folder.
# It must end with /.
# For files on the same domain, start with /.
# If an output file is at [OUTPUT_ROOT]/abc/def.png,
# the absolute URL path should be [WEB_URL_ROOT]abc/def.png.
WEB_URL_ROOT = "/tripos-notes/"

#  ------------------------------------------
# Ignore the following if you don't want to touch

# Specify the output path of a particular file `vaultPath` in the vault.
# Return None if you want to use the default algorithm to generate the output path.
# The parameters `vaultRootPath` and `outputRootPath` are passed for your convenience.
def outputPathOverride(vaultPath: Path, vaultRootPath: Path, outputRootPath: Path) -> Optional[Path]:
    if vaultPath.relative_to(vaultRootPath) == Path("Lectures/Moses's Maths Notes.md"):
        return outputRootPath / "index.html"
    return None

# Specify a list of custom HTML classes for markdown embeds based on the path `vaultPath` of the markdown file in the vault.
# For instance, you can set a custom class for all embeds with names starting with "Definition" and use CSS to give it a special colour.
# Just return [] if you don't know what this is for.
def customEmbedClasses(vaultPath: Path) -> list[str]:
    if vaultPath.stem.startswith("Definition"):
        return ["embed-definition"]

    exampleWords = ["Example", "Examples"]
    if any(vaultPath.stem.startswith(word) for word in exampleWords):
        return ["embed-example"]

    resultWords = ["Lemma", "Corollary", "Proposition", "Theorem"]
    if any(vaultPath.stem.startswith(word) for word in resultWords):
        return ["embed-result"]

    return []

# List of all Python modules (files) used to parse a markdown file.
# The modules will be imported at runtime.
# 
# When you put your module here,
# implement a global function `register()`, which should look like this:
# ```py
# from node import Node
# import parsing
# def parseMyStuff(input: str) -> list[Node]:
#     pass
#
# def register():
#     parsing.inlineParsers[myRegex] = parseMyStuff
#     # OR
#     parsing.lineStartParsers[myRegex] = parseMyStuff
# ```
# `inlineParsers` is for elements within a paragraph, such as emphasis, links, math.
# `lineStartParsers` is for block elements, such as headings, quotes, tables.
PARSER_MODULE_NAMES = [
    "parsers.comment",
    "parsers.newline",
    "parsers.math",
    "parsers.heading",
    "parsers.quote",
    "parsers.rule",
    "parsers.formatting",
    "parsers.wikilink",
    "parsers.external_link",
    "parsers.list",
    "parsers.table",
    "parsers.block_id",
]
