import re, subprocess, os, sys

src = open('/home/z/my-project/download/istoriya-rossii.html', encoding='utf-8').read()
m = re.search(r'<script>(.*?)</script>', src, re.S)
if not m:
    sys.exit('NO SCRIPT FOUND')
js = m.group(1)
os.makedirs('/tmp/jscheck', exist_ok=True)
open('/tmp/jscheck/app.js', 'w', encoding='utf-8').write(js)
r = subprocess.run(['node', '--check', '/tmp/jscheck/app.js'], capture_output=True, text=True)
print('node --check exit:', r.returncode)
print(r.stderr or 'JS syntax OK')

# quick sanity greps
for token in ['QUESTIONS', 'renderHome', 'onChecked', 'sfx.deny', 'JS_PART']:
    print(token, '->', len(re.findall(token, js)))
# count questions per level
for level in ['easy', 'medium', 'hard']:
    block = re.search(level + r': \[(.*?)\n  \]', js, re.S)
    n = len(re.findall(r"\{ t:'", block.group(1))) if block else 0
    print(level, 'questions:', n)
# check every question has expl
nq = len(re.findall(r"t:'(choice|tf|order|blank|match)'", js))
ne = len(re.findall(r"expl:", js))
print('questions with types:', nq, ' explanations:', ne)
# balanced braces rough check
print('braces {', js.count('{'), '}', js.count('}'))
