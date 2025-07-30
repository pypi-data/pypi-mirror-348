python3 -m build
twine upload dist/*
# If there is some error, check we twine check dist/*