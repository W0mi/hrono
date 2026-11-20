# Patch: calm looping background melody (Web Audio, no external files) + sound button toggles music & sfx.
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

# 1) Resume suspended context in tone() too (first tap on some browsers)
rep('''    actx = actx || new (window.AudioContext || window.webkitAudioContext)();
    const t = actx.currentTime + (dt||0);''',
'''    actx = actx || new (window.AudioContext || window.webkitAudioContext)();
    if(actx.state==='suspended') actx.resume();
    const t = actx.currentTime + (dt||0);''')

# 2) MUSIC module after sfx
rep("  win(){ [523.25, 659.25, 783.99, 1046.5].forEach((f,i)=>tone(f, 0.16, i*0.12)); }\n};",
'''  win(){ [523.25, 659.25, 783.99, 1046.5].forEach((f,i)=>tone(f, 0.16, i*0.12)); }
};

/* ================= Спокойная фоновая мелодия (свой синтез, без файлов) ================= */
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
})();''')

# 3) Sound button toggles music + effects
rep('''$('soundBtn').addEventListener('click',()=>{
  muted=!muted;
  try{ localStorage.setItem('histRu_muted', muted?'1':'0'); }catch(e){}
  renderTop();
  if(!muted) sfx.tap();
});''',
'''$('soundBtn').addEventListener('click',()=>{
  muted=!muted;
  try{ localStorage.setItem('histRu_muted', muted?'1':'0'); }catch(e){}
  renderTop();
  if(muted){ MUSIC.stop(); } else { sfx.tap(); MUSIC.start(); }
});''')

# 4) Start music on first user gesture (browser autoplay policy)
rep("renderTop();\n$('owlEntry').innerHTML=owl('happy',110);",
'''document.addEventListener('pointerdown',()=>{ if(!muted) MUSIC.start(); });
renderTop();
$('owlEntry').innerHTML=owl('happy',110);''')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
