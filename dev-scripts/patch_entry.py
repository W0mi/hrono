# Patch: entry screen with two choices — feed the bear / play.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) Entry screen HTML instead of active home
rep('  <section id="screen-home" class="screen active">',
'''  <section id="screen-entry" class="screen active">
    <div class="entrywrap">
      <span id="owlEntry"></span>
      <h1>Привет! Чем займёмся?</h1>
      <p class="entrysub">Выбирай: угостить медведя Михайло — или отправиться покорять эпохи.</p>
      <div class="entrycards">
        <button class="entrycard ec-bear" id="entryBear">
          <span class="ec-ava"><img id="bearAva" alt="Медведь Михайло"></span>
          <span class="ec-txt"><span class="ec-t">Покормить мишку</span><span class="ec-s">Михайло Потапыч уже проголодался</span></span>
        </button>
        <button class="entrycard ec-play" id="entryPlay">
          <span class="ec-ava">🎮</span>
          <span class="ec-txt"><span class="ec-t">Поиграть</span><span class="ec-s">8 эпох · 288 вопросов · собери короны</span></span>
        </button>
      </div>
    </div>
  </section>

  <section id="screen-home" class="screen">''')

# 2) CSS for the entry screen
rep('.epoch,.diffcard,.opt,.chip,.slot,.mitem,.sbox,.modal,.home-note{box-shadow:0 2px 10px rgba(95,58,23,.10)}',
'''.epoch,.diffcard,.opt,.chip,.slot,.mitem,.sbox,.modal,.home-note{box-shadow:0 2px 10px rgba(95,58,23,.10)}

/* ===== Entry screen ===== */
.entrywrap{display:flex;flex-direction:column;align-items:center;text-align:center;padding:36px 24px 30px}
.entrywrap h1{font-size:23px;margin:10px 0 6px;font-weight:800;color:#4a3220}
.entrysub{margin:0 0 26px;color:#6b4a2f;font-size:14.5px;line-height:1.45;max-width:300px}
.entrycards{width:100%;max-width:340px;display:flex;flex-direction:column;gap:14px}
.entrycard{display:flex;align-items:center;gap:14px;width:100%;background:#fff;border:2px solid var(--border);border-bottom-width:6px;border-radius:18px;padding:14px 16px;cursor:pointer;font-family:inherit;text-align:left;transition:transform .06s,border-color .15s}
.entrycard:hover{border-color:#c99e63}
.entrycard:active{transform:translateY(3px);border-bottom-width:3px}
.ec-ava{width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;flex:none;overflow:hidden}
.ec-ava img{width:100%;height:100%;object-fit:cover}
.ec-bear .ec-ava{background:#f6e3c8;border:2px solid #e3c9a4}
.ec-play .ec-ava{background:var(--blue-bg);border:2px solid #b5e3f9}
.ec-txt{display:flex;flex-direction:column}
.ec-t{font-weight:800;font-size:17px;color:#4a3220}
.ec-s{font-size:13px;color:#7a5a3a;margin-top:3px}''')

# 3) goEntry + bearFrom
rep("function goHome(){ renderHome(); renderTop(); show('screen-home'); }",
'''function goHome(){ renderHome(); renderTop(); show('screen-home'); }
let bearFrom='top';
function goEntry(){ renderTop(); show('screen-entry'); }''')

# 4) listeners: entry buttons + bear back target
rep("$('bearBtn').addEventListener('click', openBear);",
'''$('bearBtn').addEventListener('click', ()=>{ bearFrom='top'; openBear(); });
$('entryBear').addEventListener('click', ()=>{ sfx.tap(); bearFrom='entry'; openBear(); });
$('entryPlay').addEventListener('click', ()=>{ sfx.tap(); goHome(); });''')

rep("$('bearBack').addEventListener('click', ()=>{ sfx.tap(); goHome(); });",
    "$('bearBack').addEventListener('click', ()=>{ sfx.tap(); (bearFrom==='entry')?goEntry():goHome(); });")

# 5) init: open entry screen, paint owl + bear avatar
rep("renderTop();\nrenderHome();\ncheckHibernation();",
'''renderTop();
$('owlEntry').innerHTML=owl('happy',110);
$('bearAva').src=BEAR_AVATAR;
goEntry();
checkHibernation();''')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
