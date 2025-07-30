import pytest

import shpg


def test_html_elements():
    # Headings
    assert(shpg.Heading1("Hello world!").to_html() == '<h1>Hello world!</h1>')
    assert(shpg.Heading1("Hello world!").to_html() == shpg.H1('Hello world!').to_html())
    assert(shpg.Heading2("Hello world!").to_html() == '<h2>Hello world!</h2>')
    assert(shpg.Heading2("Hello world!").to_html() == shpg.H2('Hello world!').to_html())
    assert(shpg.Heading3("Hello world!").to_html() == '<h3>Hello world!</h3>')
    assert(shpg.Heading3("Hello world!").to_html() == shpg.H3('Hello world!').to_html())
    assert(shpg.Heading4("Hello world!").to_html() == '<h4>Hello world!</h4>')
    assert(shpg.Heading4("Hello world!").to_html() == shpg.H4('Hello world!').to_html())
    assert(shpg.Heading5("Hello world!").to_html() == '<h5>Hello world!</h5>')
    assert(shpg.Heading5("Hello world!").to_html() == shpg.H5('Hello world!').to_html())
    assert(shpg.Heading6("Hello world!").to_html() == '<h6>Hello world!</h6>')
    assert(shpg.Heading6("Hello world!").to_html() == shpg.H6('Hello world!').to_html())

    # Paragraph
    assert(shpg.Paragraph("Hello world!").to_html() == '<p>Hello world!</p>')
    
    # Links
    assert(shpg.Link("linktosomewhere", "Hello world!").to_html() == '<a href="linktosomewhere">Hello world!</a>')
    assert(shpg.Link("linktosomewhere", "Hello world!").to_html() == shpg.A("linktosomewhere", "Hello world!").to_html())

    # Images
    assert(shpg.Image("pathtotheimage").to_html() == '<img src="pathtotheimage" />')
    assert(shpg.Image("pathtotheimage").to_html() == shpg.Img("pathtotheimage").to_html())

    # Structural
    assert(shpg.Div().to_html() == '<div></div>')
    assert(shpg.Div(id="thisisanid").to_html() == '<div id="thisisanid"></div>')
    assert(shpg.Div("Simple text").to_html() == '<div>Simple text</div>')
    assert(shpg.Div(shpg.Paragraph("Simple text")).to_html() == '<div><p>Simple text</p></div>')

    assert(shpg.Section().to_html() == '<section></section>')

    # Table
    assert(shpg.Table().to_html() == '<table></table>')
    assert(shpg.Table([[0, 1], [2, 3]]).to_html() == '<table><tbody><tr><td>0</td><td>1</td></tr><tr><td>2</td><td>3</td></tr></tbody></table>')
    # TODO: need more tests on tables

    # TODO: add test for lists
    
    