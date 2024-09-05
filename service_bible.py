from fasthtml.common import *

from bible import word_search, get_bible, Verses
from bible import get_cmd, exec_cmd

START_PAGE = "@PSA 45 2-5"

bs = Style(':root {color:white; background:black;}')
ws = Style(':root {color:black; background:white;}')
app = FastHTML()
rt = app.route

PAGE_STYLE = "padding:100px; border: 1px solid;  max-height:1000px; overflow-y:scroll;"

@rt("/")
def get(sess):
    card = Card(Div(cmd(START_PAGE, sess)),id='result')
    form = Card(Form(
            Input(id="cmd", placehold="Command"),
            Button('enter'),
            hx_post='/cmd',target_id='result',
            hx_swap='beforeend', hx_on__after_request='document.querySelector("#result > :last-child").scrollIntoView(true)',
            ),
                style="position:sticky; top:0; background: white;"
            )
    return form,card

@app.post("/cmd")
def cmd(cmd:str, sess):
    lcmd = sess.get('lcmd',None)
    print(f'cmd: {cmd}; lcmd: {lcmd}')
    if cmd[0] in '#@' and cmd == lcmd:
        return None
    if cmd[0] == 'c':
        if cmd == 'cb':
            app.hdrs.append(bs)
        if cmd == 'cw':
            app.hdrs.append(ws)
        return None
    result = exec_cmd(cmd, lcmd=sess.get('lcmd', None))
    sess['lcmd'] = cmd
    #print(result)
    if type(result) is Verses:
        verses = Div(*list(map(lambda v: Div(Span(v[0][0],style="color:#888"),v[1]), result.verses)))
        result = Div(Div(result.book, result.get_book(), result.chapter, style="color:#888"), verses)
    elif result:
        verses = Div(*list(map(lambda v: Div(Span(v[2],v[1],v[0],style="color:#888"),v[3]), result)))
        result = Div(verses)
    if result:
        result = Div(Div(cmd),result, id=f'{cmd}', style=PAGE_STYLE)
    return result

serve(port=5051)
