from lxml import etree


root_pl = etree.parse('../bible/Polish2018Bible.xml')

def get_root():
    return root_pl

def get_bible(book, chapter, verses):
    if verses:
        pass


book = 1
chapter = 1

xpath_expression = f".//book[@number='{book}']//chapter[@number='{chapter}']//verse"
elements = get_root().xpath(xpath_expression)

print(repr(elements))
if len(elements) > 0:
    print(dir(elements[0]))
    for e in elements:
        print (e.text)


