# Patch: rename mascot bear Михайло -> Хроно (protect historical Михайлович/Михайлов in quiz data).
import re
HTML = '/home/z/my-project/download/istoriya-rossii.html'
html = open(HTML, encoding='utf-8').read()

before = html.count('Михайло')
# bare "Михайло" (not followed by a Cyrillic letter) -> "Хроно"; leaves Михайлович/Михайлов intact
html, cnt = re.subn(r'Михайло(?![а-яёА-ЯЁ])', 'Хроно', html)
print('renamed bare Михайло:', cnt, 'of', before)

# tidy: full name becomes just Хроно; natural phrases
pairs = [
    ('Хроно Потапыч', 'Хроно'),
    ('угостить медведя Хроно', 'угостить Хроно'),
    ('Покормить мишку', 'Покормить Хроно'),
    ('в магазине медведя', 'у Хроно в магазине'),
]
n = 0
for old, new in pairs:
    c = html.count(old)
    assert c >= 1, 'NOT FOUND: ' + old
    html = html.replace(old, new)
    n += c
    print(old, '->', new, 'x', c)

left = re.findall(r'Михайло[а-яёА-ЯЁ]*', html)
print('leftover Михайло* forms:', left)
assert all(f != 'Михайло' for f in left), 'bare Михайло left!'
assert len(left) == 4, 'unexpected historical form count'
assert 'Михайлович' in html and 'Михайлов' in html, 'historical names damaged!'

open(HTML, 'w', encoding='utf-8').write(html)
print('phrase fixes:', n)
