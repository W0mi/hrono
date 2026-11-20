# Patch: bear tamagotchi + shop (balalaikas) + daily gift + hints + hibernation.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:80]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:80]
    html = html.replace(old, new, 1)
    n += 1

# ---------- 1) CSS ----------
CSS = '''
/* ===== Bear tamagotchi & shop ===== */
.stat.bal{color:#c07a00}
.bearhead{display:flex;flex-direction:column;align-items:center;text-align:center;padding:10px 24px 6px}
.bearring{width:112px;height:112px;border-radius:50%;background:radial-gradient(circle at 50% 38%,#8a5a30 0%,#5a3517 74%);border:5px solid #e9b45c;box-shadow:0 8px 18px rgba(95,58,23,.35),inset 0 0 14px rgba(255,214,130,.45);display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative;transition:filter .3s}
.bearring img{width:86px;height:86px;border-radius:50%;object-fit:cover}
.bearring.sleep{filter:brightness(.55) saturate(.5)}
.bearring.sleep::after{content:'💤';position:absolute;font-size:24px;right:-4px;bottom:-6px}
.bearring.fed{animation:fedpop .55s ease}
@keyframes fedpop{40%{transform:scale(1.1)}}
.bearname{font-size:19px;font-weight:800;color:#4a3220;margin-top:10px}
.bearstatus{font-size:14px;font-weight:700;color:#6b4a2f;margin-top:3px;min-height:18px}
.satbar{width:100%;max-width:300px;height:16px;background:rgba(255,255,255,.6);border:2px solid #d9bd97;border-radius:8px;overflow:hidden;margin-top:10px}
.satfill{height:100%;width:0%;background:#58a700;border-radius:8px;transition:width .4s ease}
.satlbl{font-size:11.5px;font-weight:800;letter-spacing:.6px;color:#7a5a3a;margin-top:5px;text-transform:uppercase}
.balrow{display:flex;align-items:center;justify-content:center;gap:7px;margin-top:10px;font-weight:800;font-size:18px;color:#4a3220}
.sleepcard{margin:12px 24px 0;padding:14px 16px;background:#fff;border:2px solid var(--border);border-radius:14px;font-size:13.5px;color:#6b4a2f;line-height:1.5;text-align:center;box-shadow:0 2px 10px rgba(95,58,23,.10)}
.gift{margin:12px 24px 0;padding:13px 16px;background:#fff;border:2px dashed #e0a53c;border-radius:14px;text-align:center;font-weight:700;font-size:13.5px;color:#7a5230;line-height:1.5}
.gift b{color:#c07a00}
.shopgrid{display:flex;flex-direction:column;gap:12px;padding:14px 24px 30px}
.shopcard{display:flex;align-items:center;gap:13px;background:#fff;border:2px solid var(--border);border-bottom-width:5px;border-radius:16px;padding:13px 15px}
.shopcard .sico{width:50px;height:50px;border-radius:12px;background:#f6ead6;display:flex;align-items:center;justify-content:center;font-size:25px;flex:none}
.shopcard .st1{font-weight:800;font-size:15.5px}
.shopcard .st2{font-size:12.5px;color:#777;margin-top:2px;line-height:1.35}
.sbuy{margin-left:auto;flex:none;border:none;background:var(--green);color:#fff;font-weight:800;font-size:13.5px;padding:10px 13px;border-radius:12px;border-bottom:4px solid var(--green-dark);cursor:pointer;font-family:inherit;text-transform:uppercase;letter-spacing:.4px}
.sbuy:active:not(:disabled){transform:translateY(2px);border-bottom-width:2px}
.sbuy:disabled{background:#e5e5e5;border-bottom-color:#d0d0d0;color:#b7b7b7;cursor:default}
.hintbtn{width:100%;margin-top:12px;background:#fff;border:2px solid var(--blue);border-bottom-width:4px;color:var(--blue-dark);font-weight:800;font-size:14px;padding:10px;border-radius:14px;cursor:pointer;font-family:inherit}
.hintbtn:active:not(:disabled){transform:translateY(1px)}
.hintbtn:disabled{border-color:var(--border);color:var(--muted);cursor:default;background:#fff}
.opt.out{opacity:.32;pointer-events:none}
</style>'''
rep('</style>', CSS)

# ---------- 2) Topbar: balalaika stat + bear button ----------
rep('''    <div class="stat bolt" title="Всего XP">⚡<span id="stXp">0</span></div>
    <button class="iconbtn" id="soundBtn" title="Звук">🔊</button>''',
'''    <div class="stat bolt" title="Всего XP">⚡<span id="stXp">0</span></div>
    <div class="stat bal" title="Балалайки">🪕<span id="stBal">0</span></div>
    <button class="iconbtn" id="bearBtn" title="Тамагочи: медведь Михайло">🧸</button>
    <button class="iconbtn" id="soundBtn" title="Звук">🔊</button>''')

# ---------- 3) New screens ----------
SCREENS = '''  <!-- BEAR TAMAGOTCHI -->
  <section id="screen-bear" class="screen">
    <div class="backrow"><button class="backbtn" id="bearBack">← Назад</button></div>
    <div class="bearhead">
      <div class="bearring" id="bearRing"><img id="bearImg" alt="Медведь Михайло"></div>
      <div class="bearname">Михайло Потапыч</div>
      <div class="bearstatus" id="bearStatus"></div>
      <div class="satbar"><div class="satfill" id="satFill"></div></div>
      <div class="satlbl" id="satLbl"></div>
      <div class="balrow">🪕 <span id="bearBal">0</span> балалаек</div>
    </div>
    <div class="sleepcard" id="sleepCard" style="display:none"></div>
    <div class="foot-btns" style="max-width:330px">
      <button class="btn" id="feedBtn">🍎 Покормить</button>
      <button class="btn" id="honeyBtn" style="display:none">🍯 Угощение мёдом</button>
      <button class="btn btn-blue" id="shopBtn">🛒 Магазин балалаек</button>
    </div>
  </section>

  <!-- SHOP -->
  <section id="screen-shop" class="screen">
    <div class="backrow"><button class="backbtn" id="shopBack">← Назад к медведю</button></div>
    <div class="diffhead">
      <h1 style="font-size:22px">Магазин</h1>
      <div class="years">Балалайки — местная валюта. Заходи каждый день — подарок растёт!</div>
      <div class="balrow">🪕 <span id="shopBal">0</span></div>
    </div>
    <div class="gift" id="giftBox"></div>
    <div class="shopgrid" id="shopList"></div>
  </section>

  <!-- LESSON -->'''
rep('  <!-- LESSON -->', SCREENS)

# ---------- 4) loadStore with defaults merge ----------
rep('''function loadStore(){
  try{ return JSON.parse(localStorage.getItem('histRu_store')) || {xp:0, streak:0, lastDay:null, done:{}}; }
  catch(e){ return {xp:0, streak:0, lastDay:null, done:{}}; }
}''',
'''function loadStore(){
  const def = {xp:0, streak:0, lastDay:null, done:{}, bal:0, hints:0, food:0, honey:0,
               bear:{sat:70, lastFeed:null, sleepUntil:null}, shopG:{last:null, day:0}};
  try{
    const s = JSON.parse(localStorage.getItem('histRu_store')) || {};
    const st = Object.assign({}, def, s);
    st.bear  = Object.assign({}, def.bear,  s.bear  || {});
    st.shopG = Object.assign({}, def.shopG, s.shopG || {});
    st.done  = s.done || {};
    return st;
  }catch(e){ return JSON.parse(JSON.stringify(def)); }
}''')

# ---------- 5) renderTop: balalaika count ----------
rep("  $('stXp').textContent = store.xp;",
    "  $('stXp').textContent = store.xp;\n  $('stBal').textContent = store.bal||0;")

# ---------- 6) Bear & shop logic + hint ----------
BEAR = '''function goHome(){ renderHome(); renderTop(); show('screen-home'); }

/* ================= ТАМАГОЧИ: МЕДВЕДЬ И МАГАЗИН ================= */
const FOODS = [
  { key:'apple', icon:'🍎', name:'Яблоко',   desc:'Простая еда: +40 к сытости Михайло',            cost:2, sat:40 },
  { key:'honey', icon:'🍯', name:'Мёд',      desc:'Любимое лакомство: сразу +100 к сытости',       cost:5, sat:100 },
  { key:'hint',  icon:'💡', name:'Подсказка', desc:'Убирает один неверный вариант в вопросе урока', cost:3 }
];
function todayStr(){ return new Date().toDateString(); }
function daysBetween(a,b){ return Math.floor((new Date(b) - new Date(a))/86400000); }
function bearSleeping(){ return !!(store.bear.sleepUntil && new Date(store.bear.sleepUntil) > new Date()); }
function satietyNow(){
  let sat = store.bear.sat;
  if(store.bear.lastFeed) sat -= daysBetween(store.bear.lastFeed, Date.now())*20;
  return Math.max(0, Math.min(100, sat));
}
function checkHibernation(){
  if(!store.lastDay) return;
  if(daysBetween(store.lastDay, Date.now()) >= 2 && !bearSleeping()){
    store.bear.sleepUntil = new Date(Date.now()+3*86400000).toISOString();
    store.bear.sat = Math.min(store.bear.sat, 50);
    saveStore();
    toast('🐻 Михайло уснул в спячку на 3 дня — ты пропустил заходы!');
  }
}
function renderBear(){
  const sleeping = bearSleeping(), sat = satietyNow();
  $('bearImg').src = BEAR_AVATAR;
  $('bearRing').classList.toggle('sleep', sleeping);
  $('bearBal').textContent = store.bal;
  const fill=$('satFill');
  fill.style.width = sat+'%';
  fill.style.background = sat>=70 ? '#58a700' : (sat>=35 ? '#e6a700' : '#ea2b2b');
  $('satLbl').textContent = sleeping ? 'Спячка 💤' : 'Сытость: '+sat+' / 100';
  const sc=$('sleepCard'), fb=$('feedBtn'), hb=$('honeyBtn');
  if(sleeping){
    const left = Math.max(1, Math.ceil((new Date(store.bear.sleepUntil) - Date.now())/86400000));
    sc.style.display='block';
    sc.innerHTML='🐻‍❄️ <b>Спячка.</b> Стрик заходов был сорван — Михайло ушёл спать на три дня.<br>Проснётся через <b>'+left+'</b> '+(left===1?'день':'дня')+'. Заходи каждый день, чтобы медведь не спал!';
    fb.disabled=true; fb.textContent='😴 Михайло спит';
    hb.style.display='none';
    $('bearStatus').textContent='Михайло крепко спит…';
  } else {
    sc.style.display='none';
    $('bearStatus').textContent = sat>=70 ? 'Доволен и готов к урокам!' : sat>=35 ? 'Немного проголодался…' : 'Очень голоден! Купи еду в магазине.';
    fb.disabled = store.food<=0;
    fb.textContent = store.food>0 ? '🍎 Покормить ('+store.food+')' : '🍎 Нет еды — зайди в магазин';
    hb.style.display = store.honey>0 ? 'block' : 'none';
    if(store.honey>0) hb.textContent = '🍯 Угощение мёдом ('+store.honey+')';
  }
}
function openBear(){ sfx.tap(); checkHibernation(); renderBear(); show('screen-bear'); }
function feedBear(kind){
  if(bearSleeping()){ sfx.deny(); return; }
  const have = kind==='honey' ? store.honey : store.food;
  if(have<=0){ sfx.deny(); toast('Нет еды — купи в магазине 🛒'); return; }
  if(kind==='honey') store.honey--; else store.food--;
  store.bear.sat = Math.min(100, satietyNow() + (kind==='honey'?100:40));
  store.bear.lastFeed = Date.now();
  saveStore(); sfx.tap();
  const ring=$('bearRing'); ring.classList.remove('fed'); void ring.offsetWidth; ring.classList.add('fed');
  toast(kind==='honey' ? 'Михайло уплетает мёд! 🍯' : 'Михайло сыт! 🍎');
  renderBear();
}
function giftForDay(d){ return Math.min(d,5); }
function openShop(){ sfx.tap(); renderShop(); show('screen-shop'); }
function renderShop(){
  const today = todayStr(), box=$('giftBox');
  if(store.shopG.last !== today){
    const yest = new Date(Date.now()-86400000).toDateString();
    store.shopG.day = (store.shopG.last===yest) ? store.shopG.day+1 : 1;
    store.shopG.last = today;
    const amt = giftForDay(store.shopG.day);
    store.bal += amt;
    saveStore();
    box.innerHTML = '🎁 <b>Дневной подарок: +'+amt+' 🪕</b> — день '+store.shopG.day+' подряд. Заходи каждый день: 1-й день — 1 балалайка, 2-й — 2… и до 5 в день!';
  } else {
    box.innerHTML = '🎁 Дневной подарок уже получен сегодня. Возвращайся завтра — подарок растёт каждый день подряд (до 5 🪕).';
  }
  $('shopBal').textContent = store.bal;
  const list=$('shopList'); list.innerHTML='';
  FOODS.forEach((it,idx)=>{
    const owned = it.key==='hint' ? store.hints : (it.key==='honey' ? store.honey : store.food);
    const card=document.createElement('div'); card.className='shopcard';
    card.innerHTML = '<div class="sico">'+it.icon+'</div>'
      +'<div style="flex:1"><div class="st1">'+it.name+' · '+it.cost+' 🪕'
      +(owned>0?' <span style="color:#58a700">· есть: '+owned+'</span>':'')+'</div>'
      +'<div class="st2">'+it.desc+'</div></div>'
      +'<button class="sbuy" '+(store.bal<it.cost?'disabled':'')+' data-i="'+idx+'">Купить</button>';
    card.querySelector('.sbuy').addEventListener('click',()=>buyItem(idx));
    list.appendChild(card);
  });
}
function buyItem(idx){
  const it=FOODS[idx];
  if(store.bal<it.cost){ sfx.deny(); toast('Не хватает балалаек — заходи завтра за подарком 🎁'); return; }
  store.bal -= it.cost;
  if(it.key==='hint') store.hints++;
  else if(it.key==='honey') store.honey++;
  else store.food++;
  saveStore(); sfx.tap();
  toast('Куплено: '+it.icon+' '+it.name);
  renderShop(); renderTop();
}
function useHint(q,hb){
  if(!(q.t==='choice'||q.t==='blank'||q.t==='tf') || store.hints<=0) return;
  const target=$('qbox').querySelector('.opt[data-ok="0"]:not(.out)');
  if(!target){ toast('Подсказка здесь больше не поможет'); return; }
  target.classList.add('out');
  store.hints--; saveStore(); sfx.tap();
  if(store.hints>0){ hb.textContent='💡 Подсказка: убрать неверный вариант · осталось '+store.hints; }
  else { hb.disabled=true; hb.textContent='💡 Подсказки закончились — купи в магазине медведя 🧸'; }
  toast('Неверный вариант убран 💡');
}
$('bearBtn').addEventListener('click', openBear);
$('bearBack').addEventListener('click', ()=>{ sfx.tap(); goHome(); });
$('feedBtn').addEventListener('click', ()=>feedBear('apple'));
$('honeyBtn').addEventListener('click', ()=>feedBear('honey'));
$('shopBtn').addEventListener('click', openShop);
$('shopBack').addEventListener('click', ()=>{ sfx.tap(); renderBear(); show('screen-bear'); });'''
rep("function goHome(){ renderHome(); renderTop(); show('screen-home'); }", BEAR)

# ---------- 7) Hint button in renderQ ----------
rep('''    $('checkBtn').style.display='none';
    $('contBtn').style.display='block';
    $('contBtn').disabled=true;
  }
}''',
'''    $('checkBtn').style.display='none';
    $('contBtn').style.display='block';
    $('contBtn').disabled=true;
  }

  const hintable = q.t==='choice'||q.t==='blank'||q.t==='tf';
  const hb=document.createElement('button');
  hb.className='hintbtn';
  hb.disabled = !hintable || store.hints<=0;
  hb.textContent = !hintable ? '💡 Для этого задания подсказки нет'
                 : store.hints>0 ? '💡 Подсказка: убрать неверный вариант · осталось '+store.hints
                 : '💡 Подсказок нет — купи в магазине медведя 🧸';
  hb.addEventListener('click',()=>useHint(q,hb));
  box.appendChild(hb);
}''')

# ---------- 8) Init: hibernation check ----------
rep('''renderTop();
renderHome();
</script>''',
'''renderTop();
renderHome();
checkHibernation();
</script>''')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
