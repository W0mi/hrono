# Patch: raise shop prices a bit; paid hints no longer apply to true/false (2 options = full answer reveal).
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) Prices
rep("{ key:'apple', icon:'🍎', name:'Яблоко',   desc:'Простая еда: +40 к сытости Михайло',            cost:2, sat:40 }",
    "{ key:'apple', icon:'🍎', name:'Яблоко',   desc:'Простая еда: +40 к сытости Михайло',            cost:3, sat:40 }")
rep("{ key:'honey', icon:'🍯', name:'Мёд',      desc:'Любимое лакомство: сразу +100 к сытости',       cost:5, sat:100 }",
    "{ key:'honey', icon:'🍯', name:'Мёд',      desc:'Любимое лакомство: сразу +100 к сытости',       cost:8, sat:100 }")
rep("{ key:'hint',  icon:'💡', name:'Подсказка', desc:'Убирает один неверный вариант в вопросе урока', cost:3 }",
    "{ key:'hint',  icon:'💡', name:'Подсказка', desc:'Убирает один неверный вариант в вопросе урока', cost:5 }")

# 2) Hints apply to choice/blank only (tf has 2 options — removing one reveals the answer)
rep("  if(!(q.t==='choice'||q.t==='blank'||q.t==='tf') || store.hints<=0) return;",
    "  if(!(q.t==='choice'||q.t==='blank') || store.hints<=0) return;")
rep("  const hintable = q.t==='choice'||q.t==='blank'||q.t==='tf';",
    "  const hintable = q.t==='choice'||q.t==='blank';")

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
