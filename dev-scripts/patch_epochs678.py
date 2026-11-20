# Patch: add epochs 6-8 (Царство Романовых / Российская империя / Советский период).
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:80]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:80]
    html = html.replace(old, new, 1)
    n += 1

# 1) Three new icons in the same white-on-dark style
bolt_tail = """    +'<path d="M28,5 L13,27 L22,27 L19,43 L35,19 L25.5,19 Z" fill="#fff" stroke="#32302d" stroke-width="2.4" stroke-linejoin="round"/>'
    +'</svg>',"""
icons_new = bolt_tail + """
  eagle: '<svg width="40" height="40" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">'
    +'<g fill="#fff" stroke="#32302d" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">'
    +'<path d="M20,9 L20,5.5 L22,7.5 L24,4.5 L26,7.5 L28,5.5 L28,9 Z"/>'
    +'<path d="M4,27 Q14,17.5 22,21.5 L22,28.5 Q13,31 4,27 Z"/>'
    +'<path d="M44,27 Q34,17.5 26,21.5 L26,28.5 Q35,31 44,27 Z"/>'
    +'<ellipse cx="24" cy="24" rx="5.2" ry="9.5"/>'
    +'<path d="M19,33 L24,43 L29,33 Z"/>'
    +'<circle cx="20" cy="12.5" r="3.1"/>'
    +'<circle cx="28" cy="12.5" r="3.1"/>'
    +'<path d="M17,12 L13,13.2 L17,14.4 Z"/>'
    +'<path d="M31,12 L35,13.2 L31,14.4 Z"/>'
    +'</g></svg>',
  palace: '<svg width="40" height="40" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">'
    +'<g fill="#fff" stroke="#32302d" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">'
    +'<path d="M24,6 L43,17 L5,17 Z"/>'
    +'<rect x="9" y="19.5" width="30" height="2.6"/>'
    +'<rect x="12" y="24.5" width="4.6" height="13"/>'
    +'<rect x="21.7" y="24.5" width="4.6" height="13"/>'
    +'<rect x="31.4" y="24.5" width="4.6" height="13"/>'
    +'<rect x="7" y="39.5" width="34" height="3.6" rx="1.6"/>'
    +'</g></svg>',
  star: '<svg width="40" height="40" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">'
    +'<path d="M24,4.5 L29.4,16.8 L42.8,18.1 L32.7,27 L35.9,40.2 L24,33.2 L12.1,40.2 L15.3,27 L5.2,18.1 L18.6,16.8 Z" fill="#fff" stroke="#32302d" stroke-width="2.2" stroke-linejoin="round"/>'
    +'</svg>',"""
rep(bolt_tail, icons_new)

# 2) Three epoch cards
rep("  { icon:'bolt', title:'Смутное время',              years:'1598–1613', locked:true }",
    """  { icon:'bolt', title:'Смутное время',              years:'1598–1613', locked:true },
  { icon:'eagle', title:'Царство Романовых',          years:'1613–1721', locked:false },
  { icon:'palace', title:'Российская империя',        years:'1721–1917', locked:false },
  { icon:'star',  title:'Советский период',           years:'1917–1991', locked:false }""")

# 3) Home note
rep('📚 Вопросы составлены по конспекту «1.docx»: открыты все эпохи — Древнерусское государство (862–1132), Период раздробленности (1132–1237), Ордынское владычество (1237–1480) и Московское государство (1480–1584). Соберите три короны в каждой!',
    '📚 Вопросы составлены по конспекту «1.docx»: открыты эпохи 1–4 и 6–8 — Древнерусское государство, Раздробленность, Ордынское владычество, Московское государство, Царство Романовых (1613–1721), Российская империя (1721–1917) и Советский период (1917–1991). Смутное время откроется позже!')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
