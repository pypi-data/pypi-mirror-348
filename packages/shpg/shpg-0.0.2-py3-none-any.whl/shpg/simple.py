from .html import *
from .page import create_tmp_tag, TempTagType, Page, DEFAULT_TITLE, StyleSheets


class SimpleHeader(Div):
    """A header with a title and a menu bar."""

    def __init__(self, title: str, menu_dict: dict = None, **attributes) -> None:
        super().__init__(**attributes)
        self.attributes['class'] = "header"
        self.append(Heading1(title))
        if menu_dict:
            self.append(SimpleHMenu(menu_dict))


class SimpleFooter(Div):
    """A footer with a message and site map."""

    def __init__(self, message: str = None, links_dict: dict = None, **attributes) -> None:
        super().__init__(**attributes)
        self.attributes['class'] = "footer"
        if message:
            self.append(message)
        if links_dict:
            self.append(SimpleSiteMap(links_dict))
        self.append(Paragraph(
            'Generated with <a target="_blank" href="https://github.com/BastienCagna/shpg">Static HTML Page Generator</a>.'))


class SimpleDictVTable(HTMLTag):
    """Convert dict to a HTML table with one key-item pair by line."""

    def __init__(self, data: str, **attributes) -> None:
        super().__init__('table', **attributes)
        self.data = data

    def inner_html(self) -> str:
        inner = ''
        for k, v in self.data.items():
            inner += '<tr><th>{}</th><td>{}</td>'.format(
                to_html(k), to_html(v))
        return inner


def _generate_submenu(items, depth=0):
    """Return HTML script with temporary link tags."""
    inner = '<ul' + (' class="sub-hmenu"' if depth > 0 else '') + '>'
    for label, item in items.items():
        inner += '<li>'
        if isinstance(item, dict):
            inner += label + _generate_submenu(item, depth+1)
        else:
            inner += create_tmp_tag(TempTagType.LINK, id=item.id, label=label)
        inner += '</li>'
    return inner + '</ul>'


class SimpleHMenu(Div):
    def __init__(self, items: dict = None, **attributes) -> None:
        super().__init__(**attributes)
        self.attributes['class'] = 'hmenu'
        self.items = items or {}
        self.children = []

    def append(self, k, item):
        self.items[k] = item

    def inner_html(self) -> str:
        return _generate_submenu(self.items)


class SimpleSiteMap(Div):
    def __init__(self, links_dict: dict, **attributes) -> None:
        super().__init__(**attributes)
        self.attributes['class'] = 'sitemap'
        self.links = links_dict or {}

    def inner_html(self) -> str:
        html = ''
        for title, links in self.links.items():
            html += '<div><h4>' + title + '</h4>'
            if isinstance(links, dict):
                html += '<ul>'
                for label, item in links.items():
                    html += '<li>' + \
                        create_tmp_tag(TempTagType.LINK,
                                       id=item.id, label=label) + '</li>'
                html += '</ul>'
            else:
                html += links.to_html()
            html += "</div>"
        return html


class SimpleToolTip(HTMLTag):
    def __init__(self, label: HTMLTag, tooltip: HTMLTag, **attributes) -> None:
        super().__init__("div", classname="tooltip", **attributes)
        self.children = [label, Div(tooltip, classname="tooltiptext")]


class SimplePage(Page):
    def __init__(self, title: str = DEFAULT_TITLE, content=None, menu: dict = None, footer_msg: str = None,
                 blocks={}, stylesheet: 'str|StyleSheets|list' = StyleSheets.DEFAULT) -> None:
        super().__init__(title, content, blocks, stylesheet)
        self.header = SimpleHeader(title, menu)
        self.footer = SimpleFooter(footer_msg)

    def to_html(self, data: dict = ...) -> str:
        memo = self.content
        self.content = [self.header, self.content, self.footer]
        html = super().to_html(data)
        self.content = memo
        return html
