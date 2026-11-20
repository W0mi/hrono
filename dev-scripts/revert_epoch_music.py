# Revert: remove per-epoch tracks, restore single menu melody module and plain show().
HTML = '/home/z/my-project/download/istoriya-rossii.html'
PATCH = '/home/z/my-project/scripts/patch_epoch_music.py'

src = open(PATCH, encoding='utf-8').read()
old_module = src.split("OLD_MODULE = '''")[1].split("'''")[0]
new_module = src.split("NEW_MODULE = '''")[1].split("'''")[0]

html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) swap MUSIC module back
rep(new_module, old_module)

# 2) remove track selection from show()
rep('''  window.scrollTo(0,0);
  let tr='menu';
  if(id==='screen-diff'||id==='screen-lesson'||id==='screen-result'||id==='screen-over') tr='ep'+(L.epoch||0);
  MUSIC.set(tr);
}''',
'''  window.scrollTo(0,0);
}''')

open(HTML, 'w', encoding='utf-8').write(html)
print('reverted patches:', n)
