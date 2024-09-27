from lxml import etree
from dataclasses import dataclass, field

from func_tools import log_call
from func_tools import xpath_range
from func_tools import gen_book_map


chpt = gen_book_map()
        

@dataclass
class Verses:
    book : int
    chapter : int
    #verse : field(default_factory=list)
    #verses : list[tuple] = []
    #keyword : str = None
    
    verses: list = field(default_factory=list)
    def get_book(self): return chpt[self.book-1]
    def __str__(self):
        bk = chpt[self.book-1]
        result = []
        for v in self.verses:
            result.append(f'({self.book}){bk}.{self.chapter}.{v[0]}: {v[1]}')
        return '\n'.join(result)
    def ref(self):
        return f'({self.book}) {chpt[self.book-1]} {self.chapter}' 

#TODO
#from func_tools import files_in

#srcs = files_in('../bible/')
#for res in srcs:

root = None
roots = []

@log_call
def load_translations():
    global root
    global roots

    root_pl = etree.parse('../bible/Polish2018Bible.xml')
    root_pl2 = etree.parse('../bible/PolishNPDBible.xml')
    #root_pl3 = etree.parse('../bible/PolishBible.xml')
    #root_pl4 = etree.parse('../bible/PolishGdanskBible.xml')
    root_en = etree.parse('../bible/EnglishNIVBible.xml')

    roots = [ 
             root_pl, 
             #root_pl2,
             #root_pl3,
             #root_pl4,
             root_en ]
    root = roots[0]

load_translations()

#root = root_pl

def get_root():
    return root
def swap_root():
    global root
    root = roots[(roots.index(root) + 1)% len(roots)]#NC:3]
    

def encapsulate(verse):
    v = Verse(int(verse.getparent().getparent().values()[0]),
              int(verse.getparent().values()[0]),
              [int(verse.values()[0])])


@log_call
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
	locations = list(map(lambda l: (l.values()[0], l.getparent().values()[0],
                                 chpt[int(l.getparent().getparent().values()[0])-1], l.text), locations))
    #location = list(map( lambda l: encapsulate(
	return locations



@log_call
def get_bible(book, chapter, verses):
    xpath_expr = f"//book[@number='{book}']//chapter[@number='{chapter}']"
    #xpath_expr = xpath_expr + f"//verse[@number >={start} and @number <={end}]"
    #if verses:
    xpath_expr = xpath_expr + f"//verse"+xpath_range('number',verses)

    print(xpath_expr)
    elements = get_root().xpath(xpath_expr)
    result = list(map(lambda elem: (elem.values(), elem.text), elements))
    return Verses(book,chapter,result)

def get_cmd(cmd):
    cmd = cmd[1:].strip().split(' ')
    book = cmd[0]
    if not book.isnumeric():
        book = chpt.index(book.upper()) + 1
    else:
        book = int(book)
    chapter = int(cmd[1])

    verses = []
    if len(cmd) == 3:
        vs = cmd[2].split(',')
        for v in vs:
            if '-' in v:
                vfrom,vto = v.split('-')
                v = (int(vfrom), int(vto))
            else:
                v = int(v)
            verses.append(v)

    result = get_bible(book,chapter,verses)
    #print(result)
    #print("="*60)
    return result

def seek_cmd(cmd):
    cmd = cmd[1:]
    r = word_search(cmd)
    print(r)
    if r:
        for el in r :
            print(el)
    return r

def exec_cmd(cmd, lcmd = ''):
    if 's' == cmd:
        swap_root()
        if '@' in lcmd:
            return get_cmd(lcmd)
    elif '@' in cmd: 
        lcmd = cmd
        return get_cmd(cmd)
    elif '#' in cmd:
        lcmd = cmd
        return seek_cmd(cmd)

def cmd_ui():

    lcmd = ''
    scmd = ''
    print("="*60)
    while True:
        cmd = input('>')
        if cmd in chpt:
            ...
        exec_cmd(cmd, lcmd)


def test_lib():
    r = get_bible(1,2,[4,7,(10,12)])
    #r = get_bible(1,2,[4])
    #r = list(r)
    #print(dir(r[0]))
    #print(repr(r))
    print(repr(r))
    r2 = word_search('test')
    print(r2)

if __name__ == '__main__':
    test_lib()
    cmd_ui()

