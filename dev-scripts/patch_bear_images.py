# Patch: full-height bear images (eating honey / sleeping when sat<30) on tamagotchi screen.
import base64, io
from PIL import Image

HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0

def b64jpeg(path, max_side=640, quality=82):
    im = Image.open(path).convert('RGB')
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

EAT = b64jpeg('/home/z/my-project/scripts/assets/bear_eat4.png')
SLEEP = b64jpeg('/home/z/my-project/scripts/assets/bear_sleep.png')
print('eat kb:', len(EAT)//1024, 'sleep kb:', len(SLEEP)//1024)

def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:80]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:80]
    html = html.replace(old, new, 1)
    n += 1

# 1) Image constants
rep('''function owl(mood, size){
  size = size||110;''',
"const BEAR_EAT='"+EAT+"';\nconst BEAR_SLEEP='"+SLEEP+"';\nfunction owl(mood, size){\n  size = size||110;")

# 2) CSS: circular avatar -> full-height figure card
rep(".bearring{width:112px;height:112px;border-radius:50%;background:radial-gradient(circle at 50% 38%,#8a5a30 0%,#5a3517 74%);border:5px solid #e9b45c;box-shadow:0 8px 18px rgba(95,58,23,.35),inset 0 0 14px rgba(255,214,130,.45);display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative;transition:filter .3s}",
    ".bearring{width:220px;max-width:76vw;border-radius:22px;background:radial-gradient(circle at 50% 35%,#8a5a30 0%,#5a3517 74%);border:5px solid #e9b45c;box-shadow:0 8px 18px rgba(95,58,23,.35),inset 0 0 14px rgba(255,214,130,.45);display:flex;align-items:flex-end;justify-content:center;overflow:hidden;position:relative;transition:filter .3s}")
rep(".bearring img{width:86px;height:86px;border-radius:50%;object-fit:cover}",
    ".bearring img{width:100%;height:auto;display:block}")

# 3) renderBear: image + drowsy state
rep("""  $('bearImg').src = BEAR_AVATAR;
  $('bearRing').classList.toggle('sleep', sleeping);""",
"""  const hungrySleep = !sleeping && sat < 30;
  $('bearImg').src = (sleeping || hungrySleep) ? BEAR_SLEEP : BEAR_EAT;
  $('bearRing').classList.toggle('sleep', sleeping || hungrySleep);""")

# 4) Labels
rep("  $('satLbl').textContent = sleeping ? 'Спячка 💤' : 'Сытость: '+sat+' / 100';",
    "  $('satLbl').textContent = sleeping ? 'Спячка 💤' : (hungrySleep ? 'Спит от голода 💤 · Сытость: '+sat+' / 100' : 'Сытость: '+sat+' / 100');")
rep("    $('bearStatus').textContent = sat>=70 ? 'Доволен и готов к урокам!' : sat>=35 ? 'Немного проголодался…' : 'Очень голоден! Купи еду в магазине.';",
    "    $('bearStatus').textContent = sat>=70 ? 'Доволен и уплетает мёд!' : sat>=30 ? 'Немного проголодался…' : 'Михайло уснул от голода! Разбуди мёдом 🍯';")

# 5) Feeding wakes the drowsy bear
rep("""function feedBear(kind){
  if(bearSleeping()){ sfx.deny(); return; }
  const have = kind==='honey' ? store.honey : store.food;
  if(have<=0){ sfx.deny(); toast('Нет еды — купи в магазине 🛒'); return; }""",
"""function feedBear(kind){
  if(bearSleeping()){ sfx.deny(); return; }
  const wasDrowsy = satietyNow() < 30;
  const have = kind==='honey' ? store.honey : store.food;
  if(have<=0){ sfx.deny(); toast('Нет еды — купи в магазине 🛒'); return; }""")
rep("  toast(kind==='honey' ? 'Михайло уплетает мёд! 🍯' : 'Михайло сыт! 🍎');",
    "  toast(wasDrowsy ? '🍯 Мёд разбудил Михайло!' : (kind==='honey' ? 'Михайло уплетает мёд! 🍯' : 'Михайло сыт! 🍎'));")

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
