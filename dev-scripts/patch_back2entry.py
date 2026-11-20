# Patch: remove tiny topbar arrow; add medium back button inside the "play" (epochs) screen.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) Remove topbar arrow button
rep('''    <button class="iconbtn homebtn" id="homeBtn" title="На главный экран" style="display:none">←</button>
    <button class="iconbtn" id="soundBtn" title="Звук">🔊</button>''',
    '    <button class="iconbtn" id="soundBtn" title="Звук">🔊</button>')

# 2) Remove its CSS
rep('''.iconbtn{background:none;border:none;font-size:18px;cursor:pointer;padding:4px}
.homebtn{color:var(--blue);font-weight:800;font-size:20px;padding:2px 8px}''',
    '.iconbtn{background:none;border:none;font-size:18px;cursor:pointer;padding:4px}')

# 3) Remove visibility toggle from show()
rep('''  window.scrollTo(0,0);
  const hb=$('homeBtn');
  if(hb) hb.style.display=['screen-home','screen-diff','screen-bear','screen-shop'].includes(id)?'flex':'none';
}''',
'''  window.scrollTo(0,0);
}''')

# 4) Replace listener: topbar homeBtn -> homeBack on the epochs screen
rep("$('homeBtn').addEventListener('click', ()=>{ sfx.tap(); goEntry(); });",
    "$('homeBack').addEventListener('click', ()=>{ sfx.tap(); goEntry(); });")

# 5) Back row at the top of the play (epochs) screen
rep('''  <section id="screen-home" class="screen">
    <div class="hero">''',
'''  <section id="screen-home" class="screen">
    <div class="backrow"><button class="backbtn" id="homeBack">← Назад</button></div>
    <div class="hero">''')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
