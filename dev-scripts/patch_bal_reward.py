# Patch: +1 balalaika for every correct answer (with badge in praise and live topbar counter).
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) Award +1 balalaika on each correct answer
rep('''  if(ok){
    L.correct++; L.xpGain += DIFFS[L.level].xp;
    fb.className='fb fb-ok';''',
'''  if(ok){
    L.correct++; L.xpGain += DIFFS[L.level].xp;
    store.bal = (store.bal||0) + 1;
    saveStore(); renderTop();
    fb.className='fb fb-ok';''')

# 2) Badge in the praise line
rep("      +PRAISE[Math.floor(Math.random()*PRAISE.length)]+'</div><div class=\"fx\">'+esc(q.expl)+'</div></div>';",
    "      +PRAISE[Math.floor(Math.random()*PRAISE.length)]+' <span class=\"btag\">+1 🪕</span></div><div class=\"fx\">'+esc(q.expl)+'</div></div>';")

# 3) Badge CSS
rep('.ec-s{font-size:13px;color:#7a5a3a;margin-top:3px}',
'''.ec-s{font-size:13px;color:#7a5a3a;margin-top:3px}
.btag{display:inline-block;background:#fff3c4;border:1px solid #e8d48a;border-radius:10px;padding:1px 8px;margin-left:6px;font-size:13px;color:#7a5200;vertical-align:middle}''')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
