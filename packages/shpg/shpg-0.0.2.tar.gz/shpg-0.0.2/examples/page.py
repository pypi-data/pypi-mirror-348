"""
.. _page:

===========================================================================================
Render a single page containing a Matplotlib figure and a custom reprensentation of dataset
===========================================================================================
"""

import shpg
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
import os.path as op
import webbrowser


# Create a plot
x = np.linspace(0, 10, 500)
y = np.sin(x)
fig, ax = plt.subplots()
line1, = ax.plot(x, y, label='a line')
line2, = ax.plot(x, y - 0.2, dashes=[6, 2], label='Using the dashes parameter')
ax.legend()
fig_path = "/tmp/html_report_fig.png"
fig.savefig(fig_path)

plot_section = shpg.Section(
    shpg.Heading2("Random result figure"),
    fig_path    # Image will be automatically detected, could also create shpg.Image object
)

# Create fake data
subjects = [
    {'name': "Subject 1", 'age': 12, 'volume': 80,
        'image': '/tmp/html_report/images/img001.jpg'},
    {'name': "Subject 2", 'age': 39, 'volume': 120,
        'image': '/tmp/html_report/images/img002.jpg'},
    {'name': "Subject 3", 'age': 40, 'volume': 110,
        'image': '/tmp/html_report/images/img003.jpg'},
]

# Create a custom display to print each sample of the fake data
class SubjectSection(shpg.Section):
    def __init__(self, subject: dict) -> None:
        super().__init__()
        # Start with the name of the subject has header
        self.append(shpg.Heading3(subject['name']))
        # Add a table that show some properties of the subject
        self.append(shpg.SimpleDictVTable(
            {'Age': subject['age'], 'Cortical volume': subject['volume']}))
        # Add an image of the subject
        # self.add(shpg.Image(subject['image']))

subjects_section = shpg.Section(shpg.Heading2("Subjects"))
for sub in subjects:
    subjects_section.append(SubjectSection(sub))


# Create the HTML Page
page = shpg.Page(title="HTML Report Example")
page.content.append(shpg.Heading1("HTML Report Example"))
page.content.append(shpg.Paragraph('This is an example to show some features of the package. <a href="https://fr.wikipedia.org/wiki/NeuroSpin">Here is a link to go somewhere</a>'))
page.content.append(plot_section)
page.content.append(subjects_section)

# Save the html page with a local copy of the plot
report_path = "/tmp/html_report_example.html"
page.save(report_path, portable=True)

# Open it in the browser
webbrowser.open('file://' + op.realpath(report_path))
