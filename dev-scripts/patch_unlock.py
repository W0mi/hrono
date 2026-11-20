# Patch: epochs unlock progressively — epoch N+1 opens only after all 3 levels of epoch N are done.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) Unlock rule + dynamic renderHome
rep("function renderHome(){\n  const path=$('epochPath'); path.innerHTML='';\n  EPOCHS.forEach((ep,idx)=>{",
'''function epUnlocked(idx){
  if(idx===0) return true;
  const LVL=['easy','medium','hard'];
  return LVL.every(k=>store.done[(idx-1)+'.'+k]||((idx-1)===0&&store.done[k]));
}
function renderHome(){
  const path=$('epochPath'); path.innerHTML='';
  EPOCHS.forEach((ep,idx)=>{
    const locked=!epUnlocked(idx);''')

rep("    const cls = ep.locked ? 'lock' : (crowns===3 ? 'done' : 'open');",
    "    const cls = locked ? 'lock' : (crowns===3 ? 'done' : 'open');")
rep("    el.className='epoch'+(ep.locked?' lock':'');",
    "    el.className='epoch'+(locked?' lock':'');")
rep("'<button class=\"node '+cls+'\"><span>'+(ep.locked?EPICONS.lock:EPICONS[ep.icon])+'</span>'",
    "'<button class=\"node '+cls+'\"><span>'+(locked?EPICONS.lock:EPICONS[ep.icon])+'</span>'")
rep("      +'<div class=\"epstatus'+(ep.locked?' lock':'')+'\">'\n      +(ep.locked?'Скоро в следующих уроках':(crowns===3?'Эпоха пройдена полностью! 👑👑👑':(crowns>0?'Нажмите, чтобы продолжить':'Нажмите, чтобы начать')))+'</div></div>';",
"      +'<div class=\"epstatus'+(locked?' lock':'')+'\">'\n      +(locked?'🔒 Пройди все 3 уровня предыдущей эпохи':(crowns===3?'Эпоха пройдена полностью! 👑👑👑':(crowns>0?'Нажмите, чтобы продолжить':'Нажмите, чтобы начать')))+'</div></div>';")
rep("      if(ep.locked){ sfx.deny(); toast('🔒 Эта эпоха появится в следующих уроках'); return; }",
    "      if(locked){ sfx.deny(); toast('🔒 Сначала пройди все 3 уровня предыдущей эпохи'); return; }")

# 2) Safety guard in openDiff
rep("function openDiff(idx){\n  L.epoch=idx;",
'''function openDiff(idx){
  if(!epUnlocked(idx)){ sfx.deny(); toast('🔒 Эпоха ещё закрыта'); return; }
  L.epoch=idx;''')

# 3) Update the home note describing progression
rep('<div class="home-note">📚 Вопросы составлены по конспекту «1.docx»: открыты все 8 эпох — от Древнерусского государства (862–1132) до Советского периода (1917–1991). Смутное время (1598–1613) — по конспекту! Соберите три короны в каждой!</div>',
    '<div class="home-note">📚 Вопросы составлены по конспекту «1.docx». Сначала открыта 1-я эпоха: пройди в ней все три уровня — 🌱 легкий, 📚 средний и 🎓 высокий — и откроется следующая эпоха. Так, шаг за шагом, дойдёшь от Древнерусского государства (862–1132) до Советского периода (1917–1991)! Собери три короны в каждой эпохе!</div>')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
