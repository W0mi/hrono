# Patch: topbar arrow button -> entry (greeting) screen; hidden where it makes no sense.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) Topbar: arrow before the sound button
rep('    <button class="iconbtn" id="soundBtn" title="Звук">🔊</button>',
'''    <button class="iconbtn homebtn" id="homeBtn" title="На главный экран" style="display:none">←</button>
    <button class="iconbtn" id="soundBtn" title="Звук">🔊</button>''')

# 2) CSS
rep('.iconbtn{background:none;border:none;font-size:18px;cursor:pointer;padding:4px}',
'''.iconbtn{background:none;border:none;font-size:18px;cursor:pointer;padding:4px}
.homebtn{color:var(--blue);font-weight:800;font-size:20px;padding:2px 8px}''')

# 3) show(): toggle arrow visibility per screen
rep('''function show(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  $(id).classList.add('active');
  window.scrollTo(0,0);
}''',
'''function show(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  $(id).classList.add('active');
  window.scrollTo(0,0);
  const hb=$('homeBtn');
  if(hb) hb.style.display=['screen-home','screen-diff','screen-bear','screen-shop'].includes(id)?'flex':'none';
}''')

# 4) listener
rep("$('entryPlay').addEventListener('click', ()=>{ sfx.tap(); goHome(); });",
'''$('entryPlay').addEventListener('click', ()=>{ sfx.tap(); goHome(); });
$('homeBtn').addEventListener('click', ()=>{ sfx.tap(); goEntry(); });''')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
