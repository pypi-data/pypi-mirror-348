from enum import Enum
import os.path as op
from os import makedirs
import shutil
import typing
from typing import List
from os import listdir
import json
from warnings import warn
from .html import HTMLProvider, Div, HTMLTag, get_chidrens_tags, generate_html_tag


INDEX_DIRNAME = "index"
INDEX_FILENAME = "index.html"
CONTENT_DIRNAME = "content"
PAGES_DIRNAME = "pages"
DEFAULT_TITLE = "Untitled page"


def find_urls(html: str, attributes=["src", "href"]) -> List[str]:
    """Return all the URL content in the HTML script.

    Parameters
    ----------
    html: str
        HTML script.

    attributes: list of str, defauft=['src', 'href']
        The parser look only to tag containing those attributes to find urls.

    Return
    ------
    urls: list of str
        List of the URLs.
    """
    urls = []
    for attr in attributes:
        parts = html.split(attr + "=")
        for p in parts[1:]:
            p = p.strip()
            if p[0] == "'":
                urls.append(p.split("'")[1])
            elif p[0] == '"':
                urls.append(p.split('"')[1])
            else:
                pass
    return urls


def find_content_urls(string: str) -> List[str]:
    """Same as find_urls but do not return URLs to distant content."""
    results = []
    for url in find_urls(string):
        if url.startswith("http://") or url.startswith("https://"):
            continue
        results.append(url)
    return results


def make_script_portable(html: str, abs_target_path: str, rel_target_path: str) -> str:
    """Copy linked content to the target_path and update the URLs in the script"""
    files = find_content_urls(html)

    for f in set(files):
        original_dir, fname = op.split(f)
        # If the file is not from the target directory
        abs_original_dir = op.abspath(original_dir)
        if abs_original_dir != abs_target_path and not abs_original_dir.startswith(
            abs_target_path
        ):
            # If a file with same name is present, increment the filename
            orig_fname = fname
            name, ext = op.splitext(orig_fname)
            i = 0
            while fname in listdir(abs_target_path):
                fname = "{}{:d}{}".format(name, i, ext)
                i += 1
            new_abs_path = op.join(abs_target_path, fname)
            new_rel_path = op.join(rel_target_path, fname)

            if op.exists(f):
                shutil.copy(f, new_abs_path)

            # Then, replace filename occurance in the html script
            html = html.replace(f, new_rel_path)
    return html


def create_index_dir(parent_dir: str):
    """Create the index directory and erase it if already existing."""
    index_dir = op.join(parent_dir, INDEX_DIRNAME)
    if op.exists(index_dir):
        shutil.rmtree(index_dir)

    makedirs(index_dir, exist_ok=True)
    return index_dir


TEMP_TAG_START_DELIMITER = "$[$"
TEMP_TAG_END_DELIMITER = "$]$"


class TempTagType(Enum):
    UNKNOWN = 0
    LINK = 1


def create_tmp_tag(type: TempTagType, **data):
    data["_tag_type"] = type.value
    data_str = json.dumps(data)
    return "{}{}{}".format(TEMP_TAG_START_DELIMITER, data_str, TEMP_TAG_END_DELIMITER)


def generate_tag(serialized_tmp_tag: str, items: List[HTMLProvider]) -> str:
    data = json.loads(serialized_tmp_tag.split(TEMP_TAG_START_DELIMITER)[-1])
    t = TempTagType(data["_tag_type"])

    if t == TempTagType.LINK:
        link = None
        for item in items:
            if item.id == data["id"]:
                if isinstance(item, Page):
                    link = item.filename
                else:
                    raise NotImplementedError(
                        "If HTML tag of a page, it should link as an anchor"
                    )
                break
        if not link:
            raise ValueError("Cannot find item {}".format(data["id"]))
        return generate_html_tag("a", data["label"], href=link)
    raise NotImplementedError("Unknown tak type or not implemented decoding.")


def _decode_first_temporary_tag(html: str, items: List[HTMLProvider]) -> str:
    parts = html.split(TEMP_TAG_END_DELIMITER)
    if len(parts) > 1:
        ppart = parts[0].split(TEMP_TAG_START_DELIMITER)
        out = "".join(ppart[:-1])
        if len(ppart) > 1:
            out += generate_tag(ppart[-1], items)
        else:
            raise ValueError(
                "Wrong pre-formatted HTML: Failed to find starting bound of temporary tag."
            )
        return out + TEMP_TAG_END_DELIMITER.join(parts[1:])
    return None


def decode_tmp_tags(html: str, items: List[HTMLProvider]) -> str:
    new_html = _decode_first_temporary_tag(html, items)
    while new_html:
        html = new_html
        new_html = _decode_first_temporary_tag(html, items)
    return html


class StyleSheets(Enum):
    DEFAULT = "default.css"


def fill_slots(element, slot_id, tag):
    if isinstance(element, (list, tuple)):
        new_elements = []
        for e in element:
            new_elements.append(fill_slots(e, slot_id, tag))
        return new_elements
    elif isinstance(element, HTMLProvider):
        element.fill_slots(slot_id, tag)
    return element


class Page(HTMLProvider):
    """
    A Page can generate the HTML script of a full web page.

    Parameters
    ----------
    title: str
    content: HTMLTag | list of HTMLTag
    blocks: dict
    stylesheet: str | StyleSheets | list of str | list of StyleSheets
        HTML Stylesheet aims to be a .css file or a CSS string content.
    """

    def __init__(
        self,
        title: str = DEFAULT_TITLE,
        content=None,
        blocks={},
        stylesheet: "str|StyleSheets|list" = StyleSheets.DEFAULT,
        header_js: List[str] = None,
        body_js: List[str] = None,
    ) -> None:
        super().__init__()
        self.title = title
        if content:
            self.content = content
        else:
            self.content = Div([], classname="page")
        self.stylesheet = stylesheet
        self.header_js = header_js or []
        self.body_js = body_js or []
        self.blocks = blocks
        self.filename = None

    def link(self, label: str, **attributes) -> str:
        return create_tmp_tag(TempTagType.LINK, id=self.id, label=label, **attributes)

    def to_html(self, data: dict = {}) -> str:
        self.stylesheet = (
            [self.stylesheet]
            if not isinstance(self.stylesheet, (tuple, list))
            else self.stylesheet
        )
        style_html = ""
        for sheet in self.stylesheet:
            if isinstance(sheet, StyleSheets):
                style_html += '<link rel="stylesheet" href="{}">'.format(
                    op.realpath(op.join(op.split(__file__)[0], "style", sheet.value))
                )
            else:
                if op.exists(sheet):
                    style_html += f'<link rel="stylesheet" href="{sheet}">'
                else:
                    style_html += f"<style>{sheet}</style>"

        js_html = ""
        for js in self.header_js:
            if op.isfile(js) or js.startswith("http"):
                js_html += f'<script type="text/javascript" src="{js}"></script>'
            else:
                js_html += f"<script>{js}</script>"

        js_body_html = ""
        for js in self.body_js:
            if op.isfile(js) or js.startswith("http"):
                js_body_html += f'<script type="text/javascript" src="{js}"></script>'
            else:
                js_body_html += f"<script>{js}</script>"

        if isinstance(self.content, list):
            body = Div(*self.content, classname="page").to_html()
        else:
            body = self.content.to_html()

        html = f"<html><head><title>{self.title}</title>{js_html}{style_html}</head><body>{body}{js_body_html}</body>"
        # TODO: process template to input data
        return html

    # def set_filename(self, filename, root:str=None):
    #     self.filename = filename
    # self.root = root

    def get_relative_path_to(self, filename):
        if not self.filename:
            raise ValueError(
                "Page filename should be set before requesting relative paths"
            )
        return op.relpath(filename, op.split(self.filename)[0])
        # if not root:
        #     self.path_from_root = './'
        #     self.path_to_root = './'
        # else:
        #     self.path_from_root = relpath(filename, op.abspath(op.split(root)[0]))
        #     self.path_to_root = relpath(root, op.abspath(op.split(filename)[0]))

    def save(
        self,
        filename: str = None,
        portable=False,
        index_dir: str = None,
        items: List[HTMLProvider] = None,
        blocks={},
    ):
        if filename:
            self.filename = filename

        # Replace HTMLSlots if HTMLProviders are specified
        if len(blocks):
            tmp_blocks = self.blocks
            for id, tag in blocks.items():
                tmp_blocks[id] = tag
            blocks = tmp_blocks
        else:
            blocks = self.blocks
        for slot_id, tag in self.blocks.items():
            self.content = fill_slots(self.content, slot_id, tag)
            # for element in self.content:
            #     element.fill_slots(slot_id, tag)

        # Generate HTML script
        html = self.to_html()

        # Decode temporary tags
        if not items:
            items = get_chidrens_tags(self.content)
        html = decode_tmp_tags(html, items)

        if portable:
            parent_dir, fname = op.split(filename)
            if not index_dir:
                index_dir = create_index_dir(parent_dir)
            content_dir = op.join(index_dir, CONTENT_DIRNAME)
            makedirs(content_dir, exist_ok=True)
            html = make_script_portable(
                html, op.abspath(content_dir), op.relpath(content_dir, parent_dir)
            )

        with open(filename, "w") as f:
            f.write(html)


class Book:
    """
    A book is a set of pages sharing header and footer.

    Parameters
    ----------
    title: str
        Title of the book.
    index: Page
        Index page (home page) of the book.
    pages: list of Page
        Set of pages of the book.
    header: HTMLTag, default=None
        First HTMLTag of each page.
    footer: HTMLTag, default=None
        Last HTMLTag of each page.
    blocks: dict
        Set of string id and HTMLTag to replace the HTMLSlot by those tag
        at rendering time.
    stylesheet: str | StyleSheets | list of str | list of StyleSheet
        see Page class.
    """

    def __init__(
        self,
        title: str = DEFAULT_TITLE,
        index=None,
        pages=[],
        header=None,
        footer=None,
        blocks={},
        stylesheet: "str|StyleSheets|list" = StyleSheets.DEFAULT,
    ) -> None:
        self.title = title
        self.stylesheet = stylesheet
        self.index = index if index else Page(title, stylesheet=stylesheet)
        self.pages: List[Page] = pages
        # TODO: if not None, use header and footer for each page when saving
        self.header = header
        self.footer = footer
        self.blocks = blocks

    def save(self, path: str, portable=False, index_dir: str = None):
        if not index_dir:
            index_dir = create_index_dir(path)
        content_dir = op.join(index_dir, CONTENT_DIRNAME)
        makedirs(
            content_dir, exist_ok=True
        )  # TODO: remove , "exist_ok=True" when lustre problem will be gone
        pages_dir = op.join(index_dir, PAGES_DIRNAME)
        makedirs(
            pages_dir, exist_ok=True
        )  # TODO: remove , "exist_ok=True" when lustre problem will be gone

        items: List[HTMLProvider] = [self.index] + get_chidrens_tags(self.index.content)
        for page in self.pages:
            page.filename = op.join(pages_dir, page.title.replace(" ", "_") + ".html")
            items.append(page)
            items.extend(get_chidrens_tags(page.content))
        self.index.filename = op.join(path, INDEX_FILENAME)

        for page in self.pages:
            # page.save(page.filename, portable, index_dir, items, self.blocks)
            self._save_page(page, page.filename, portable, index_dir, items)
        self._save_page(self.index, self.index.filename, portable, index_dir, items)
        # self.index.save(self.index.filename, portable, index_dir, items, self.blocks)

    def _save_page(
        self, page: Page, filename: str, portable: bool, index_dir: str, items: list
    ):
        memo = page.content
        page.content = []
        if self.header:
            page.content.append(self.header)
        page.content.append(memo)
        if self.footer:
            page.content.append(self.footer)
        page.save(filename, portable, index_dir, items, self.blocks)
        page.content = memo


class LinkToPage(HTMLTag):
    def __init__(self, page: Page, text: str, **attributes) -> None:
        super().__init__("a")
        self.text = text
        self.page = page
        self.attributes = attributes

    def to_html(self) -> str:
        return self.page.link(self.text, **self.attributes)
