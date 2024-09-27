from fasthtml.common import *

from bible import word_search, get_bible, Verses
from bible import get_cmd, exec_cmd

from func_tools import last_prefixed

START_PAGE = "@PSA 45 2-5"

bs = Style(':root {color:#999; background:#444;}')
ws = Style(':root {color:black; background:white;}')
app = FastHTML()
app.hdrs.append(bs)
rt = app.route

PAGE_STYLE = "padding:10%; border: 1px solid;"#  max-height:1000px; overflow-y:scroll;"

@rt("/")
def get(sess):
    lcmd = sess.get('lcmd', START_PAGE)
    card = Card(Div(page(lcmd, sess)), id='result')
    form = Card(Form(
            Input(id="cmd", placehold="Command"),
            Button('enter'),
            hx_post='/cmd/',target_id='result',
            hx_swap='innerHTML', hx_on__after_request='document.querySelector("#result > :last-child").scrollIntoView(true)',
            ), Button('lang', hx_get='/cmd/s', target_id='result', hx_swap='innerHTML'),
                style="position:sticky; top:0; background: #444;"
            )
    new_session = Button('new session', hx_delete="/new", hx_swap='delete', target_id='history')
    return form,card, new_session

@app.delete('/new')
def new(sess):
    sess['hist'] = []

@rt('/clear_broken')
def get(sess):
    hist = sess.get('hist',[])
    for item in hist[:]:
        result = exec_cmd(item)
        if not result:
            hist.remove(item)
    sess['hist'] = hist
    return Redirect('/')



@app.get("/cmd/{cmd}")
@app.post("/cmd/")
def page(cmd:str, sess):
    hist = sess.get('hist',[])
    lcmd = sess.get('lcmd','') # fix lcmd
    print(f'cmd: {cmd}; lcmd: {lcmd}')
    #if cmd[0] in '#@' and cmd == lcmd:
    #    print('same cmd')
    #    return None
    if cmd and cmd[0] == 'c':
        app.hdrs = list(filter(lambda e: e.tag != 'style', app.hdrs))
        if cmd == 'cb':
            app.hdrs.append(bs)
        if cmd == 'cw':
            app.hdrs.append(ws)
        return Redirect('/')

    result = exec_cmd(cmd, lcmd=lcmd)

    hist = sess.get('hist',[])

    import urllib.parse
    hlist = [ Button(f'[{el}]', 
                     hx_get=f"/cmd/{urllib.parse.quote(el)}",
                     target_id='result', hx_trigger='click', hx_swap='innerHTML')
             for el in hist ]
    hlist = Div(*hlist, id='history')

    #sess['lcmd'] = cmd
    #print(result)
    if type(result) is Verses:
        verses = Div(*list(map(lambda v: Div(Span(v[0][0],' ',style="color:#888; font-size:70%;"),v[1]), result.verses)))
        #result = Div(Div(result.book, result.get_book(), result.chapter, style="color:#888;"), verses)
        result = Div(Div(result.ref(), style="color:#888;"), verses)
    elif result:
        verses = Div(*list(map(lambda v: Div(Span(' '.join(reversed(v[0:3])),': ',style="color:#888"),v[3]), result)))
        result = Div(verses)
    if result:
        result = Div(hlist, result, id=f'{cmd}', style=PAGE_STYLE)

    if result and cmd[0] in '@#':
        if not cmd in hist:
            hist.append(cmd)
        sess['lcmd'] = cmd
    #print(hist[-5:])
    sess['hist'] = hist

    return result

serve(port=5051)
