# Patch: don't let paid hints be consumed after the answer is already checked.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) Guard inside useHint
rep("function useHint(q,hb){\n  if(!(q.t==='choice'||q.t==='blank') || store.hints<=0) return;",
    "function useHint(q,hb){\n  if(L.checked || !(q.t==='choice'||q.t==='blank') || store.hints<=0) return;")

# 2) Disable the hint button right after checking the answer
rep("  updateProgress(L.i+1);\n  markOptions(q, ok);",
    "  updateProgress(L.i+1);\n  markOptions(q, ok);\n  const hbn=document.querySelector('.hintbtn'); if(hbn) hbn.disabled=true;")

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
