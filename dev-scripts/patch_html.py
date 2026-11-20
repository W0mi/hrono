# Patch istoriya-rossii.html: replace owl mascot with bear logo, add brown theme.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
B64 = '/home/z/my-project/scripts/bear_avatar.b64'

html = open(HTML, encoding='utf-8').read()
b64 = open(B64).read().strip()
orig_len = len(html)
n = 0

def rep(old, new, count=1):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:80]
    html = html.replace(old, new, count)
    n += 1

# 1) theme-color -> brown
rep('<meta name="theme-color" content="#58cc02">',
    '<meta name="theme-color" content="#5a3517">')

# 2) favicon link
rep('<title>История России — тренажёр эпох</title>',
    '<title>История России — тренажёр эпох</title>\n<link rel="icon" id="favIcon" href="">')

# 3) root vars: cream bars
rep('--bg:#fff; --gray:#f7f7f7;', '--bg:#fffaf1; --gray:#f7f7f7;')

# 4) body -> brown gradient
rep('body{background:var(--gray);font-family:',
    'body{background:linear-gradient(180deg,#8a5a30 0%,#5a3517 55%,#43260f 100%);background-attachment:fixed;font-family:')

# 5) app column -> same brown gradient
rep('#app{width:100%;max-width:460px;background:var(--bg);',
    '#app{width:100%;max-width:460px;background:linear-gradient(180deg,#8a5a30 0%,#5a3517 55%,#43260f 100%);')

# 6) hero text on brown
rep('.hero h1{font-size:24px;margin:12px 0 6px;font-weight:800}',
    '.hero h1{font-size:24px;margin:12px 0 6px;font-weight:800;color:#fff}')
rep('.hero p{margin:0;color:#777;', '.hero p{margin:0;color:#f3e2cc;')

# 7) section title
rep('.sect-title{font-size:13px;font-weight:800;letter-spacing:1.2px;color:var(--muted);',
    '.sect-title{font-size:13px;font-weight:800;letter-spacing:1.2px;color:#e8cfa8;')

# 8) home note -> warm panel
rep('background:var(--gray);border:2px solid var(--border);border-radius:14px;font-size:13px;color:#888;',
    'background:rgba(255,250,242,.94);border:2px solid #e3c9a4;border-radius:14px;font-size:13px;color:#7a5230;')

# 9) difficulty head text on brown
rep('.diffhead h1{font-size:21px;margin:10px 0 4px;font-weight:800}',
    '.diffhead h1{font-size:21px;margin:10px 0 4px;font-weight:800;color:#fff}')
rep('.diffhead .years{color:#777;', '.diffhead .years{color:#f3e2cc;')
rep('.diffhead p{color:#777;', '.diffhead p{color:#f3e2cc;')

# 10) lesson question text on brown
rep('.instr{color:var(--blue);', '.instr{color:#ffd76a;')
rep('.qtext{font-size:20px;font-weight:800;line-height:1.35;margin:0 0 18px}',
    '.qtext{font-size:20px;font-weight:800;line-height:1.35;margin:0 0 18px;color:#fff}')
rep('.qtext .blank{color:var(--blue);letter-spacing:1px}',
    '.qtext .blank{color:#7fd0ff;letter-spacing:1px}')
rep('.qsub{font-size:14px;color:#777;', '.qsub{font-size:14px;color:#f3e2cc;')

# 11) result screen text on brown + stat boxes white
rep('.center h1{font-size:26px;font-weight:800;margin:14px 0 4px}',
    '.center h1{font-size:26px;font-weight:800;margin:14px 0 4px;color:#fff}')
rep('.center .sub{color:#777;', '.center .sub{color:#f3e2cc;')
rep('.sbox{border:2px solid var(--border);border-bottom-width:4px;border-radius:14px;padding:14px 10px}',
    '.sbox{border:2px solid var(--border);border-bottom-width:4px;border-radius:14px;padding:14px 10px;background:#fff}')

# 12) replace owl mascot function with bear logo image
start = '/* ================= МАСКОТ (сова) ================= */'
end = '/* ================= ЭПОХИ (по конспекту) ================= */'
i = html.index(start)
j = html.index(end)
new_block = (
    '/* ================= МАСКОТ (медведь-учёный) ================= */\n'
    "const BEAR_AVATAR='data:image/jpeg;base64," + b64 + "';\n"
    'function owl(mood, size){\n'
    '  size = size||110;\n'
    '  return \'<img src="\'+BEAR_AVATAR+\'" alt="Медведь-учёный" style="width:\'+size+\'px;height:\'+size+\'px;border-radius:50%;display:inline-block;box-shadow:0 0 0 3px rgba(255,214,130,.6),0 4px 10px rgba(0,0,0,.25)">\';\n'
    '}\n\n'
)
html = html[:i] + new_block + html[j:]
n += 1

# 13) favicon href
rep("$('owlMini').innerHTML=owl('normal',34);",
    "$('favIcon').href=BEAR_AVATAR;\n$('owlMini').innerHTML=owl('normal',34);")

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n, '| size:', orig_len, '->', len(html))
