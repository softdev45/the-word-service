from fasthtml.common import *

from bible import word_search, get_bible, Verses
from bible import get_cmd, exec_cmd

START_PAGE = "@PSA 45 2-5"

app = FastHTML()
rt = app.route

@rt("/")
def get():
    card = Card(Div(Div(cmd(START_PAGE)),id='result'))
    form = Form(
            Input(id="cmd", placehold="Command"),
            Button('enter'),
            hx_post='/cmd',target_id='result',
            hx_swap='innerHTML'
            )
    return card,form

@app.post("/cmd")
def cmd(cmd:str):
    result = exec_cmd(cmd)
    print(result)
    if type(result) is Verses:
        verses = Div(*list(map(lambda v: Div(Span(v[0][0],style="color:#888"),v[1]), result.verses)))
        result = Div(Div(Div(result.book, result.get_book(), result.chapter, style="color:#888"), verses), 
                   hw_swap_oob='true',id="rr", style="padding:100px; border: 1px solid;") 
    else:
        verses = Div(*list(map(lambda v: Div(Span(v[2],v[1],v[0],style="color:#888"),v[3]), result)))
        result = Div(verses)
    return result

serve(port=5051)
