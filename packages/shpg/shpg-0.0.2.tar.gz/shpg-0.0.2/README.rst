~~~~~~~~~~~~~~~~~~~~~~~~~~~
Static HTML Page Generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. image:: https://github.com/BastienCagna/shpg/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/BastienCagna/shpg/actions
   :alt: Github Actions Build Status

.. image:: https://badge.fury.io/py/shpg.svg
    :target: https://badge.fury.io/py/shpg

Installation
-------------

SHPG is avaialable on PyPI. You can then install it simply by executing the pip command:

.. code-block:: shell

    pip install shpg

If you want to contribute to development or customize the package:

.. code-block:: shell

    git clone https://github.com/BastienCagna/shpg.git
    cd shpg
    python setup.py develop
    
N.B: use --user to install the package only for you (might be mandatory depending of the rights you have)

Basic example
-------------


.. code-block:: python

    import shpg

    # Create the HTML Page
    page = shpg.Page(title="My Page")
    page.content.append(shpg.Heading1("Hello world!"))
    page.content.append(shpg.Paragraph('This is my first page using SHPG.'))

    # Generate the HTML page
    report_path = "/tmp/my_page.html"
    page.save(report_path, portable=True)


.. image:: doc/index/basic_page.png
  :width: 500
  :alt: Basic rendering


Documentation
-------------
The auto-generated online documentation is hosted at [https://bastiencagna.github.io/shpg/](https://bastiencagna.github.io/shpg).
