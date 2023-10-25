import markdown2

file = open("entries/python.md", "r")
markdown = file.read()
print(markdown)

html = markdown2.markdown(markdown)
print(html)
