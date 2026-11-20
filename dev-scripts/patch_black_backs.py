# Patch: all "back" buttons become solid black (filled) with white text; remove old per-button color hacks.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) One shared style: solid black, white text, same pressed-corner style as app buttons
rep('.backbtn{background:none;border:none;color:var(--blue);font-weight:800;font-size:15px;cursor:pointer;padding:6px 4px;font-family:inherit}',
'''.backbtn{background:#000;border:2px solid #000;border-bottom-width:5px;border-radius:14px;color:#fff;font-weight:800;font-size:15px;cursor:pointer;padding:8px 18px;font-family:inherit}
.backbtn:active{transform:translateY(1px)}''')

# 2) Drop inline color overrides (they would paint text black on black)
rep('<div class="backrow"><button class="backbtn" id="homeBack" style="color:#000">← Назад</button></div>',
    '<div class="backrow"><button class="backbtn" id="homeBack">← Назад</button></div>')
rep('<div class="backrow"><button class="backbtn" id="bearBack" style="color:#000">← Назад</button></div>',
    '<div class="backrow"><button class="backbtn" id="bearBack">← Назад</button></div>')
rep('<div class="backrow"><button class="backbtn" id="shopBack" style="color:#000">← Назад к медведю</button></div>',
    '<div class="backrow"><button class="backbtn" id="shopBack">← Назад к медведю</button></div>')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
