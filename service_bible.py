from fasthtml.common import *

from bible import word_search, get_bible, Verses
from bible import get_cmd, exec_cmd, get_ver, get_roots, get_ver_names

from func_tools import last_prefixed

START_PAGE = "@PSA 45 2-5"

bs = Style(':root {color:#999; background:#444;}')
ws = Style(':root {color:#383A41; background:#FAFAFA;}')
app = FastHTML()
app.hdrs.append(bs)
rt = app.route

PAGE_STYLE = "padding:5%; border: 1px solid;"#  max-height:1000px; overflow-y:scroll;"

@rt("/")
def get(sess):
    lcmd = sess.get('lcmd', START_PAGE)
    version_select = Button(f'change ver', hx_get='/cmd/s', target_id='result', hx_swap='innerHTML')
    versions = []
    for i,v in enumerate(get_ver_names()):
        version_select = Button(f'{v[:20]}',
                                hx_on_click="document.getElementById('vername').textContent = this.textContent",
                                hx_get=f'/cmd/s{i}', target_id='result', hx_swap='innerHTML'
                                ,style='font-size:80%;'
                                )
        versions.append(version_select)
    versions = Div(*versions, Div(get_ver(), id='vername'), style='font-size:60%; background:#444')
        
    card = Card(Div(page(lcmd, sess)), id='result')
    form = Card(Form(
            Input(id="cmd", placehold="Command"),
            Button('view'),
            #hx_trigger="keyup-enter",
            hx_post='/cmd/',target_id='result',
            hx_swap='innerHTML', hx_on__after_request='document.querySelector("#result > :last-child").scrollIntoView(true)',
            ), versions,
                style="position:sticky; top:0;"
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
    if cmd and cmd[0] == '!':
        pcmd = cmd[1:]
        app.hdrs = list(filter(lambda e: e.tag != 'style', app.hdrs))
        if pcmd == 'cb':
            app.hdrs.append(bs)
        if pcmd == 'cw':
            app.hdrs.append(ws)
        return Redirect('/')

    result = exec_cmd(cmd, lcmd=lcmd)

    hist = sess.get('hist',[])

    import urllib.parse
    hlist = [ Button(f'{el}', 
                     hx_get=f"/cmd/{urllib.parse.quote(el)}",
                     target_id='result', hx_trigger='click', hx_swap='innerHTML',
                     style="font-size:100%;padding:0px;")
             for el in hist 
             if '@' in el
             ]
    hlist = Div(*hlist, id='history',style="font-size:50%;padding:0px;")

    hlist2 = [ Button(f'{el}', 
                     hx_get=f"/cmd/{urllib.parse.quote(el)}",
                     target_id='result', hx_trigger='click', hx_swap='innerHTML',
                     style="font-size:100%;padding:0px;")
             for el in hist 
             if '#' in el
             ]
    hlist2 = Div(*hlist2, id='history',style="font-size:50%;padding:0px;")

    ver = get_ver()
    if type(result) is Verses:
        verses = Div(*list(map(lambda v: Div(Span(v[0][0],' ',style="color:#888; font-size:70%;"),v[1]), result.verses)))
        #result = Div(Div(result.book, result.get_book(), result.chapter, style="color:#888;"), verses)
        result = Div(Div(result.ref(), style="color:#888;"), verses)
    elif result:
        verses = Div(*list(map(lambda v: Div(
            Span(' '.join(reversed(v[0:3])),': ',v[3],style="color:#888",hx_get=f"/cmd/@{' '.join(reversed(v[1:3]))}", target_id='result', hx_trigger="click[shiftKey]", hx_swap='innerHTML')), result)))
        result = Div(verses)

    if result:
        result = Div(hlist,Div( result, id=f'{cmd}', style=PAGE_STYLE), hlist2)

    if result and cmd[0] in '@#':
        if not cmd in hist:
            hist.append(cmd)
        sess['lcmd'] = cmd
        print('set lcmd')

    sess['hist'] = hist

    return result

serve(port=5051)
