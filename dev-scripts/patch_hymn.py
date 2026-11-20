# Patch: replace menu pentatonic with a majestic Russian-history hymn (Glinka "Slavsya"-style chorale, PD theme, own synthesis).
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()
n = 0
def rep(old, new):
    global html, n
    assert old in html, 'NOT FOUND: ' + old[:90]
    assert html.count(old) == 1, 'NOT UNIQUE: ' + old[:90]
    html = html.replace(old, new, 1)
    n += 1

rep('''/* ================= Спокойная фоновая мелодия (свой синтез, без файлов) ================= */
const MUSIC=(function(){
  let on=false, timer=null, mg=null;
  const M2F=m=>440*Math.pow(2,(m-69)/12);
  /* мягкая пентатоника (ля минор): [старт, нота, длит., громкость] — цикл 9.6 с */
  const MELODY=[[0,64,1.4,.05],[.6,60,1.2,.045],[1.2,62,1.2,.045],[1.8,64,1.4,.05],
                [2.4,60,1.4,.05],[3.0,57,1.2,.045],[3.6,60,1.2,.045],[4.2,62,1.4,.05],
                [4.8,64,1.4,.05],[5.4,67,1.2,.045],[6.0,64,1.2,.045],[6.6,62,1.4,.05],
                [7.2,62,1.4,.05],[7.8,60,1.2,.045],[8.4,57,1.6,.05]];
  const BASS=[[0,45],[2.4,41],[4.8,48],[7.2,43]];
  const DUR=9.6;''',
'''/* ================= Фоновая музыка: величальный хорал «в духе Славься» Глинки (свой синтез, без файлов) ================= */
const MUSIC=(function(){
  let on=false, timer=null, mg=null;
  const M2F=m=>440*Math.pow(2,(m-69)/12);
  /* мелодия: [старт, нота, длит., громкость] — цикл 13.28 с */
  const MELODY=[[0,74,1.5,.045],[1.66,74,1.5,.045],[3.32,77,1.6,.047],[4.98,74,1.5,.045],
                [6.64,75,1.5,.045],[8.3,74,1.5,.045],[9.96,74,1.5,.045],[11.62,79,1.7,.05]];
  /* аккорды хорала: Gm Cm D Gm Eb D G G (финал — мажор) */
  const CHORDS=[[0,43,1.5],[0,55,1.5],[0,58,1.5],[0,62,1.5],
                [1.66,48,1.5],[1.66,55,1.5],[1.66,60,1.5],[1.66,63,1.5],
                [3.32,50,1.5],[3.32,57,1.5],[3.32,62,1.5],[3.32,66,1.5],
                [4.98,43,1.5],[4.98,55,1.5],[4.98,58,1.5],[4.98,62,1.5],
                [6.64,51,1.5],[6.64,55,1.5],[6.64,58,1.5],[6.64,63,1.5],
                [8.3,50,1.5],[8.3,57,1.5],[8.3,62,1.5],[8.3,66,1.5],
                [9.96,43,1.5],[9.96,55,1.5],[9.96,59,1.5],[9.96,62,1.5],
                [11.62,43,1.7],[11.62,55,1.7],[11.62,59,1.7],[11.62,67,1.7]];
  const DUR=13.28;''')

rep('''    MELODY.forEach(m=>note(m[1],m[0],m[2],m[3],'sine',0.02));
    BASS.forEach(b=>{ note(b[1],b[0],2.2,.035,'triangle',0.25); note(b[1]+7,b[0],2.2,.02,'triangle',0.3); });
    timer=setTimeout(schedule, DUR*1000);''',
'''    MELODY.forEach(m=>note(m[1],m[0],m[2],m[3],'triangle',0.06));
    CHORDS.forEach(c=>note(c[1],c[0],c[2],.026,'triangle',0.14));
    timer=setTimeout(schedule, DUR*1000);''')

open(HTML, 'w', encoding='utf-8').write(html)
print('patches applied:', n)
