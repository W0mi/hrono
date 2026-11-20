# Patch: keep topbar brand on one line now that homeBtn was added.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

rep('.topbar{position:sticky;top:0;z-index:10;background:var(--bg);display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:2px solid var(--border)}',
    '.topbar{position:sticky;top:0;z-index:10;background:var(--bg);display:flex;align-items:center;gap:7px;padding:12px 14px;border-bottom:2px solid var(--border)}')

rep('.brand{display:flex;align-items:center;gap:8px;font-weight:800;font-size:17px;flex:1}',
    '.brand{display:flex;align-items:center;gap:8px;font-weight:800;font-size:16px;flex:1;white-space:nowrap}')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
