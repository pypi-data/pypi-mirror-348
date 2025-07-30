
"""
.. _book:

================================================================================
Render a multipage (book) project with a header containing a header and a footer
================================================================================
"""

# Authors: Bastien Cagna <bastien.cagna@cea.fr>

# License: BSD (3-clause)
# sphinx_gallery_thumbnail_number = 2

import shpg


###############################################################################
# Initialize pages
###############################################################################
book = shpg.Book('Example website')
subpage = shpg.Page(title="Subpage 1")
book.pages.append(subpage)


###############################################################################
# Setup header and footer
###############################################################################
links = {"Home": book.index, "Sub page": subpage}
header = shpg.SimpleHeader("Example website", links)
footer = shpg.SimpleFooter("Example footer", {'Site:': links})


###############################################################################
# Add content to the main page
###############################################################################
book.index.title = 'Example website | Home'
book.index.content.append(header)
book.index.content.append(shpg.Heading2("Welcome Home!"))
book.index.content.append(shpg.Paragraph(
    "Follow this link to go to " + subpage.link("sub page")))
book.index.content.append(footer)


###############################################################################
# Add content to the second page
###############################################################################
subpage.content.append(header)
subpage.content.append(shpg.Heading2("Sub page 1"))
subpage.content.append(shpg.Paragraph("This is a sub page of the book."))
subpage.content.append(footer)


###############################################################################
# Render
###############################################################################
book.save("/tmp/example_book.html", portable=False)
