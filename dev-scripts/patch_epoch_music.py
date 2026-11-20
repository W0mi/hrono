# Patch: per-epoch classical themes (synthesized short motifs) + menu melody on entry/home/bear/shop.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

OLD_MODULE = '''/* ================= Спокойная фоновая мелодия (свой синтез, без файлов) ================= */
const MUSIC=(function(){
  let on=false, timer=null, mg=null;
  const M2F=m=>440*Math.pow(2,(m-69)/12);
  /* мягкая пентатоника (ля минор): [старт, нота, длит., громкость] — цикл 9.6 с */
  const MELODY=[[0,64,1.4,.05],[.6,60,1.2,.045],[1.2,62,1.2,.045],[1.8,64,1.4,.05],
                [2.4,60,1.4,.05],[3.0,57,1.2,.045],[3.6,60,1.2,.045],[4.2,62,1.4,.05],
                [4.8,64,1.4,.05],[5.4,67,1.2,.045],[6.0,64,1.2,.045],[6.6,62,1.4,.05],
                [7.2,62,1.4,.05],[7.8,60,1.2,.045],[8.4,57,1.6,.05]];
  const BASS=[[0,45],[2.4,41],[4.8,48],[7.2,43]];
  const DUR=9.6;
  function note(midi,dt,dur,vol,type,atk){
    if(muted||!on) return;
    try{
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      if(actx.state==='suspended') actx.resume();
      if(!mg){ mg=actx.createGain(); mg.gain.value=1; mg.connect(actx.destination); }
      const t=actx.currentTime+dt;
      const o=actx.createOscillator(), g=actx.createGain();
      o.type=type; o.frequency.value=M2F(midi);
      g.gain.setValueAtTime(0.0001,t);
      g.gain.linearRampToValueAtTime(vol,t+atk);
      g.gain.exponentialRampToValueAtTime(0.001,t+dur);
      o.connect(g); g.connect(mg);
      o.start(t); o.stop(t+dur+0.05);
    }catch(e){}
  }
  function schedule(){
    if(muted||!on) return;
    MELODY.forEach(m=>note(m[1],m[0],m[2],m[3],'sine',0.02));
    BASS.forEach(b=>{ note(b[1],b[0],2.2,.035,'triangle',0.25); note(b[1]+7,b[0],2.2,.02,'triangle',0.3); });
    timer=setTimeout(schedule, DUR*1000);
  }
  return {
    start(){ if(on||muted) return; on=true; schedule(); },
    stop(){ on=false; if(timer){ clearTimeout(timer); timer=null; } try{ if(mg){ mg.disconnect(); mg=null; } }catch(e){} },
    playing(){ return on; }
  };
})();'''

NEW_MODULE = '''/* ================= Фоновая музыка: тема меню + тема каждой эпохи (свой синтез, без файлов) =================
   Темы великих русских композиторов звучат как короткие синтезированные мотивы-настроение. */
const MUSIC=(function(){
  let on=false, timer=null, mg=null, cur='menu';
  const M2F=m=>440*Math.pow(2,(m-69)/12);
  const T={
    /* меню: мягкая пентатоника (ля минор) */
    menu:{w:'sine',aw:.02,v:.05,len:9.6,
      notes:[[0,64,1.4],[.6,60,1.2],[1.2,62,1.2],[1.8,64,1.4],[2.4,60,1.4],[3,57,1.2],[3.6,60,1.2],[4.2,62,1.4],
             [4.8,64,1.4],[5.4,67,1.2],[6,64,1.2],[6.6,62,1.4],[7.2,62,1.4],[7.8,60,1.2],[8.4,57,1.6]],
      bass:[[0,45,2.2],[2.4,41,2.2],[4.8,48,2.2],[7.2,43,2.2]]},
    /* 1. Римский-Корсаков — Шествие царя Берендея: торжественный, мерный ход */
    ep0:{w:'triangle',aw:.03,v:.05,bw:'triangle',len:14.4,
      notes:[[0,64,.55],[.6,69,.55],[1.2,71,.55],[1.8,72,1.1],[3,71,.55],[3.6,69,.55],[4.2,68,1.1],[5.4,69,1.1],
             [7.2,64,.55],[7.8,69,.55],[8.4,71,.55],[9,72,1.1],[10.2,74,.55],[10.8,72,.55],[11.4,71,1.1],[12.6,69,1.5]],
      bass:[[0,45,2.7],[3,40,2.7],[6,45,2.7],[9,43,2.7],[12,45,2.4]]},
    /* 2. Бородин — Половецкие пляски: быстрый восточный танец */
    ep1:{w:'square',aw:.01,v:.03,bw:'triangle',len:8.8,
      notes:[[0,74,.18],[.22,73,.18],[.44,74,.18],[.66,76,.18],[.88,74,.18],[1.1,72,.18],[1.32,74,.9],
             [2.42,72,.18],[2.64,71,.18],[2.86,72,.18],[3.08,74,.18],[3.3,76,.18],[3.52,77,.18],[3.74,76,.9],
             [4.84,72,.18],[5.06,71,.18],[5.28,69,.18],[5.5,71,.18],[5.72,72,.18],[5.94,74,.18],[6.16,72,.7],
             [6.86,69,.18],[7.08,70,.18],[7.3,69,.18],[7.52,67,.18],[7.74,69,.7]],
      bass:[[0,45,1.1],[2.42,43,1.1],[4.84,41,1.1],[6.86,40,1.1]]},
    /* 3. Прокофьев — Вставайте, люди русские: суровый марш-зыв */
    ep2:{w:'sawtooth',aw:.02,v:.028,bw:'triangle',len:9.9,
      notes:[[0,64,.5],[.55,64,.5],[1.1,64,.95],[2.2,69,.5],[2.75,71,.5],[3.3,72,1],[4.4,69,.5],[4.95,71,.5],
             [5.5,72,1.05],[6.7,71,.5],[7.25,69,.5],[7.8,71,.5],[8.35,64,1.4]],
      bass:[[0,45,2.2],[2.2,40,2.2],[4.4,45,2.2],[6.6,43,2.2],[8.8,45,1.1]]},
    /* 4. Мусоргский — Рассвет на Москва-реке: тихие "колокольчики" зари */
    ep3:{w:'sine',aw:.06,v:.04,bw:'sine',baw:.25,len:13.2,
      notes:[[0,76,2.2],[2.4,74,1.8],[4.4,72,2.2],[6.8,71,1.8],[8.8,69,2.6],[11.6,76,1.4]],
      bass:[[0,45,6.4],[6.4,43,6.8]]},
    /* 5. Мусоргский — Борис Годунов: тревожный набат и скорбная мелодия */
    ep4:{w:'sine',aw:.05,v:.042,bw:'sine',baw:.3,len:13,
      notes:[[1.1,74,.9],[2.3,72,.9],[3.5,71,1.3],[7,69,1.1],[8.4,67,1.1],[9.8,69,1.4]],
      bass:[[0,45,3],[3.2,52,2.8],[6.4,45,3],[9.6,50,3]]},
    /* 6. Глинка — Славься: широкая величальная хоровая */
    ep5:{w:'triangle',aw:.05,v:.028,bw:'triangle',baw:.15,len:13.28,
      notes:[[0,76,1.5],[1.66,77,1.5],[3.32,79,1.6],[4.98,76,1.5],[6.64,76,1.5],[8.3,74,1.5],[9.96,72,1.5],[11.62,76,1.6]],
      bass:[[0,60,1.5],[0,64,1.5],[0,67,1.5],[1.66,57,1.5],[1.66,60,1.5],[1.66,65,1.5],[3.32,55,1.5],[3.32,59,1.5],[3.32,62,1.5],
            [4.98,60,1.5],[4.98,64,1.5],[4.98,67,1.5],[6.64,57,1.5],[6.64,60,1.5],[6.64,64,1.5],[8.3,53,1.5],[8.3,57,1.5],[8.3,60,1.5],
            [9.96,55,1.5],[9.96,59,1.5],[9.96,62,1.5],[11.62,60,1.5],[11.62,64,1.5],[11.62,67,1.5]]},
    /* 7. Чайковский — Увертюра 1812 года: медная фанфара победы */
    ep6:{w:'sawtooth',aw:.02,v:.026,bw:'triangle',len:12,
      notes:[[0,60,.9],[1,64,.9],[2,67,.9],[3,72,1.7],[5,71,.45],[5.5,72,.45],[6,74,1.7],[8,72,.45],[8.5,71,.45],[9,72,2.4]],
      bass:[[0,36,2.4],[3,43,2.4],[6,36,2.4],[9,43,2.8]]},
    /* 8. Свиридов — «Время, вперёд!»: энергичный остинатный марш (мотив в его духе) */
    ep7:{w:'square',aw:.01,v:.03,bw:'triangle',len:7.98,
      notes:[[0,67,.16],[.19,67,.16],[.38,67,.16],[.57,70,.16],[.76,67,.16],[.95,69,.16],[1.14,70,.16],[1.33,72,.34],
             [1.9,74,.16],[2.09,74,.16],[2.28,74,.16],[2.47,72,.16],[2.66,70,.16],[2.85,69,.16],[3.04,70,.16],[3.23,67,.34],
             [3.8,74,.16],[3.99,74,.16],[4.18,74,.16],[4.37,72,.16],[4.56,70,.16],[4.75,69,.16],[4.94,70,.3],
             [5.5,67,.16],[5.69,67,.16],[5.88,67,.16],[6.07,70,.16],[6.26,72,.16],[6.45,74,.16],[6.64,72,.16],[6.83,70,.3]],
      bass:[[0,43,.4],[.95,43,.4],[1.9,43,.4],[2.85,38,.4],[3.8,43,.4],[4.75,43,.4],[5.7,43,.4],[6.65,38,.4]]}
  };
  function note(midi,dt,dur,vol,type,atk){
    if(muted||!on) return;
    try{
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      if(actx.state==='suspended') actx.resume();
      if(!mg){ mg=actx.createGain(); mg.gain.value=1; mg.connect(actx.destination); }
      const t=actx.currentTime+dt;
      const o=actx.createOscillator(), g=actx.createGain();
      o.type=type; o.frequency.value=M2F(midi);
      g.gain.setValueAtTime(0.0001,t);
      g.gain.linearRampToValueAtTime(vol,t+atk);
      g.gain.exponentialRampToValueAtTime(0.001,t+dur);
      o.connect(g); g.connect(mg);
      o.start(t); o.stop(t+dur+0.05);
    }catch(e){}
  }
  function schedule(){
    if(muted||!on) return;
    const t=T[cur]||T.menu;
    t.notes.forEach(m=>note(m[1],m[0],m[2],(m[3]!==undefined?m[3]:t.v),t.w,t.aw));
    (t.bass||[]).forEach(b=>note(b[1],b[0],b[2],(b[3]!==undefined?b[3]:t.v*0.7),t.bw||'triangle',t.baw||t.aw*3));
    timer=setTimeout(schedule, t.len*1000);
  }
  function cut(){ if(timer){ clearTimeout(timer); timer=null; } try{ if(mg){ mg.disconnect(); mg=null; } }catch(e){} }
  return {
    set(tr){ if(!T[tr]) tr='menu'; if(cur===tr) return; cur=tr; if(on&&!muted){ cut(); schedule(); } },
    start(){ if(on||muted) return; on=true; schedule(); },
    stop(){ on=false; cut(); },
    playing(){ return on; },
    current(){ return cur; }
  };
})();'''

rep(OLD_MODULE, NEW_MODULE)

# show(): pick the track by screen
rep('''function show(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  $(id).classList.add('active');
  window.scrollTo(0,0);
}''',
'''function show(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  $(id).classList.add('active');
  window.scrollTo(0,0);
  let tr='menu';
  if(id==='screen-diff'||id==='screen-lesson'||id==='screen-result'||id==='screen-over') tr='ep'+(L.epoch||0);
  MUSIC.set(tr);
}''')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
