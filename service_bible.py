from fasthtml.common import *


app = FastHTML()
rt = app.route

@rt("/")
def get():
    card = Card(Div(Div(':'),id='result'))
    form = Form(
            Input(id="cmd", placehold="Command"),
            Button('enter'),
            hx_post='/cmd',target_id='result',
            hx_swap='innerHTML'
            )
    return card,form

@app.post("/cmd")
async def cmd(cmd:str):
    print(cmd)
    return Div(cmd+"!",hw_swap_oob='true',id="rr", style="padding:100px; border: 1px solid;") 

serve(port=5051)
