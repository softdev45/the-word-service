from lxml import etree
from dataclasses import dataclass, field

def gen_book_map():
    result = []
    with open('chapter') as file:
        while l := file.readline().strip():
            result.append(l)
    return result

chpt = gen_book_map()
print(chpt)
        

@dataclass
class Verses:
    book : int
    chapter : int
    #verses : list[tuple] = []
    verses: list = field(default_factory=list)
    def __str__(self):
        bk = chpt[self.book-1]
        result = []
        for v in self.verses:
            result.append(f'({self.book}){bk}.{self.chapter}.{v[0]}: {v[1]}')
        return '\n'.join(result)


root_pl = etree.parse('../bible/Polish2018Bible.xml')


def get_root():
    return root_pl

def word_search(word):
	if len(w := word.split(',')) > 1:
		word = w[0]
	xpath_expression = f".//verse[contains(text(),'{word}')]"  #[not(contains(@id, '{ref}'))]"
	#TODO fix search
	# print(xpath_expression)
	locations = get_root().xpath(xpath_expression)  #, namespaces=ns)
	#todo fix
	# while w
	#locations = list(filter(lambda l: word.lower() in l.text.lower(), locations))
	# print('word search', word, locations)
	if len(locations) == 0:
		return []
	locations = list(map(lambda l: (l.text, l.values(), l.getparent().values(),
                                 chpt[int(l.getparent().getparent().values()[0])-1]), locations))
	return locations

def xpath_range(attr, rng):
    if type(rng) is int:
        start = end = rng
    else:
        if len(rng) == 2:
            start = rng[0]
            end = rng[1]
        else:
            start = end = rng[0]
    return f"[@{attr} >= {start} and @{attr} <= {end}]"



def get_bible(book, chapter, verses):
    xpath_expr = f".//book[@number='{book}']//chapter[@number='{chapter}']"
    #xpath_expr = xpath_expr + f"//verse[@number >={start} and @number <={end}]"
    if verses:
        xpath_expr = xpath_expr + f"//verse"+xpath_range('number',verses)

    elements = get_root().xpath(xpath_expr)
    result = list(map(lambda elem: (elem.values(), elem.text), elements))
    return Verses(book,chapter,result)


def cmd_ui():
    print("="*60)
    while True:
        cmd = input('>')
        if cmd in chpt:
            ...

        if ' ' in cmd: 
            parts = cmd.split(' ')
            if len(parts) == 3:
                b,c,v = parts
            elif len(parts) == 2:
                b,c = parts
                v = [0,1000]

            if not b.isnumeric():
                b = chpt.index(b.upper()) + 1
            if '-' in v:
                vs,ve = v.split('-')
                v = [int(vs), int(ve)]

            print(get_bible(b,c,v))
            print("="*60)


def test_lib():
    r = get_bible(1,2,[4,7])
    #r = list(r)
    #print(dir(r[0]))
    #print(repr(r))
    print(repr(r))
    print('ws')
    r2 = word_search('test')
    print(r2)

test_lib()
cmd_ui()

