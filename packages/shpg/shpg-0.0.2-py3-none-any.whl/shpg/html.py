import os.path as op
import typing
from typing import List
import imghdr
from uuid import uuid4


class HTMLProvider:
    """The most basic class which provide an id and to_html() method
    """

    def __init__(self, id: str = None) -> None:
        self.id = id or uuid4().hex[-8:]

    def to_html(self) -> str:
        raise NotImplementedError()

    def __add__(self, other) -> list:
        if isinstance(other, HTMLProvider):
            return [self, other]
        elif isinstance(other, (list, tuple)):
            return [self] + other
        raise ValueError("Added item should be a HTMLProvider or a list or tuple.")


class HTMLSlot(HTMLProvider):
    def __init__(self, id: str = None) -> None:
        super().__init__(id)

    def to_html(self) -> str:
        """Return empty string as an unused slot is kind of ghost"""
        return ""


def generate_html_tag(tagname, inner: str = None, **attributes) -> str:
    """ Return HTML script for the asked tag

    Paramaters
    ----------
    tagname: str
        HTML tag name.

    inner: str, default=None
        Inner HTML. The HTML script or text that is in the tag.

    attributes: dict
        HTML tag attributes. To specify class attribute use "classename" key
        instead as class is a reserved work in python.

    Return
    ------
    HTML formatted script.
    """
    attributes_str = ""
    for key, value in attributes.items():
        if key == "classname":
            key = "class"
        attributes_str += ' {}="{}"'.format(key, value)
    if inner is not None:
        return '<{}{}>{}</{}>'.format(tagname, attributes_str if len(attributes_str) > 0 else "", inner, tagname)
    else:
        return '<{}{} />'.format(tagname, attributes_str if len(attributes_str) > 0 else "")


def to_html(element) -> str:
    """ Return the HTML version of any object

    If object is not a HTMLProvider or an str, it use the str() function to
    provide the HTML content.

    Paramaters
    ----------
    tagname: any
        The object to convert to HTML script.

    Return
    ------
    HTML formatted script.
    """
    if isinstance(element, HTMLProvider):
        return element.to_html()
    elif isinstance(element, str):
        return element
    else:
        return str(element)


class HTMLTag(HTMLProvider):
    """ Basic class for all the HTML tags.
    Read more in the :ref:`User Guide <htmltag>`.

    "class" attribute must be replaced by "classname".

    Parameters
    ----------
    tagname : float, default=None
        HTML tag name.
    children : list of any
        The HTML tags or HTMLisable object contained by this tag.
    attributes : dict
        HTML tag attributes. To specify class attribute use "classename" key
        instead as class is a reserved work in python.
    orphan : bool, default=False
        When True, the tag has no innetr content. The tag will be like <.... />
    """

    def __init__(self, tagname: str, *children: 'List[HTMLTag]', orphan=False, **attributes) -> None:
        super().__init__(id=tagname + "_" + uuid4().hex[-8:])
        self.tagname = tagname
        self.attributes = attributes
        self.orphan = orphan
        self.children = []

        if not self.orphan:
            for child in children:
                if isinstance(child, (tuple, list)):
                    child = Div(*child)
                self.append(child)

    def append(self, child: 'HTMLTag') -> None:
        """Add child element."""
        if self.orphan:
            raise RuntimeError(
                "Cannot add item to {} as it is an orphan tag".format(self.tagname))
        if isinstance(child, HTMLProvider):
            self.children.append(child)
        elif isinstance(child, str):
            if op.exists(child) and imghdr.what(child):
                self.children.append(Image(child))
            else:
                self.children.append(child)
        else:
            raise ValueError("Invalid child.")

    def extend(self, children):
        """Add several child elements."""
        for child in children:
            self.append(child)

    def inner_html(self) -> str:
        """Render the inner HTML script."""
        if self.orphan:
            return None
        inner = ""
        for child in self.children:
            inner += to_html(child)
        return inner

    def to_html(self) -> str:
        """Render the full tag HTML script."""
        return generate_html_tag(self.tagname, None if self.orphan else self.inner_html(), **self.attributes)

    def fill_slots(self, id, tag: 'HTMLTag'):
        """Replace HTMLSlots of given id by the given tag if all children."""
        for ic, child in enumerate(self.children):
            if isinstance(child, HTMLProvider):
                if child.id == id:
                    self.children[ic] = tag
                elif isinstance(child, HTMLTag):
                    child.fill_slots(id, tag)

def get_chidrens_tags(tag: HTMLTag) -> List[HTMLTag]:
    """Return all the children of a tag as a single 1D list of HTMLTag."""
    if isinstance(tag, HTMLTag):
        tags = [tag]
        for t in tag.children:
            tags.extend(get_chidrens_tags(t))
        return tags
    return []


# Basic HTML tags
class Heading1(HTMLTag):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__('h1', text, **attributes)


class H1(Heading1):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__(text, **attributes)


class Heading2(HTMLTag):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__('h2', text, **attributes)


class H2(Heading2):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__(text, **attributes)


class Heading3(HTMLTag):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__('h3', text, **attributes)


class H3(Heading3):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__(text, **attributes)


class Heading4(HTMLTag):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__('h4', text, **attributes)


class H4(Heading4):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__(text, **attributes)


class Heading5(HTMLTag):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__('h5', text, **attributes)


class H5(Heading5):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__(text, **attributes)


class Heading6(HTMLTag):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__('h6', text, **attributes)

class H6(Heading6):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__(text, **attributes)

class Paragraph(HTMLTag):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__('p', text, **attributes)

class P(Paragraph):
    def __init__(self, text: str, **attributes) -> None:
        super().__init__(text, **attributes)

class Link(HTMLTag):
    def __init__(self, url: str, text: str, **attributes) -> None:
        super().__init__('a', text, **attributes)
        self.attributes['href'] = url

class A(Link):
    def __init__(self, url: str, text: str, **attributes) -> None:
        super().__init__(url, text, **attributes)

class Image(HTMLTag):
    def __init__(self, img_path: str, **attributes) -> None:
        super().__init__('img', src=img_path, **attributes, orphan=True)

class Img(Image):
    def __init__(self, img_path: str, **attributes) -> None:
        super().__init__(img_path, **attributes)

class Pre(HTMLTag):
    def __init__(self, *children, **attributes) -> None:
        super().__init__('pre', *children, **attributes)

class Div(HTMLTag):
    def __init__(self, *children, **attributes) -> None:
        super().__init__('div', *children, **attributes)

class Section(HTMLTag):
    def __init__(self, *children, **attributes) -> None:
        super().__init__('section', *children, **attributes)

class Table(HTMLTag):
    def __init__(self, data=None, names=None, **attributes) -> None:
        super().__init__("table", **attributes)
        self.data = data or []
        self.names = names

    def append(self, row):
        if isinstance(self.data, dict):
            raise ValueError(
                "Table has no append() method when using dict data.")
        if not len(self.data) or (len(self.data) and len(row) == len(self.data[0])):
            self.data.append(row)
        else:
            raise ValueError("Cannot add row of length {} to data array of width {}.".format(
                len(row), len(self.data[0])))

    def inner_html(self) -> str:
        if isinstance(self.data, dict):
            keys = list(self.data.keys()) if not self.names else self.names
            data = []
            for i in range(len(self.data[keys[0]])):
                data.append(list(self.data[k][i] for k in keys))
        else:
            data = self.data
            keys = self.names if self.names else None

        html = ''
        if keys:
            html += "<thead><tr>"
            for k in keys:
                html += "<th>" + to_html(k) + "</th>"
            html += "</tr></thead>"
        
        if data:
            html += "<tbody>"
            for dt in data:
                html += '<tr>'
                for ik in range(len(dt)):
                    html += "<td>" + to_html(dt[ik]) + "</td>"
                html += '</tr>'
            html += "</tbody>"
        return html

    def size(self):
        if isinstance(self.data, dict):
            width = len(self.data.keys())
            height = len(self.data[self.data.keys()[0]])
        else:
            width = len(self.data[0])
            height = len(self.data)
        return (height, width)

    def fill_slots(self, id, tag: 'HTMLTag'):
        for n, child in enumerate(self.names):
            if isinstance(child, HTMLProvider):
                if child.id == id:
                    self.names[n] = tag
                elif isinstance(child, HTMLTag):
                    child.fill_slots(id, tag)
        if isinstance(self.data, (list, tuple)):
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    child = self.data[i][j]
                    if isinstance(child, HTMLProvider):
                        if child.id == id:
                            if isinstance(self.data[i], tuple):
                                self.data[i] = list(self.data[i])
                            self.data[i][j] = tag
                        elif isinstance(child, HTMLTag):
                            child.fill_slots(id, tag)
        else:
            for k, children in self.data.items():
                for ic, child in enumerate(children):
                    if isinstance(child, HTMLProvider):
                        if child.id == id:
                            self.data[k][ic] = tag
                        elif isinstance(child, HTMLTag):
                            child.fill_slots(id, tag)


class ListItem(HTMLTag):
    def __init__(self, *children, **attributes) -> None:
        super().__init__('li', *children, **attributes)


class List(HTMLTag):
    def __init__(self, *children, **attributes) -> None:
        if isinstance(children, tuple):
            children = list(children)
        for ic, child in enumerate(children):
            if isinstance(child, (tuple, list)):
                children[ic] = ListItem(*child)
            elif not isinstance(child, ListItem):
                children[ic] = ListItem(child)
        super().__init__('ul', *children, **attributes)

    def append(self, child):
        if not isinstance(child, ListItem):
            raise ValueError(
                "Only ListItem could be added to List. {} given.".format(type(child)))
        return super().append(child)

    def extend(self, children):
        for child in children:
            if not isinstance(child, ListItem):
                raise ValueError(
                    "Only ListItem could be added to List. {} given.".format(type(child)))
        return super().extend(children)
