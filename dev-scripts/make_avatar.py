from PIL import Image
import base64

src = '/home/z/my-project/download/medved-logotip-kruzhok.png'
im = Image.open(src).convert('RGB')
im = im.resize((256, 256), Image.LANCZOS)
out_jpg = '/home/z/my-project/scripts/bear_avatar.jpg'
im.save(out_jpg, 'JPEG', quality=88, optimize=True)
b64 = base64.b64encode(open(out_jpg, 'rb').read()).decode()
open('/home/z/my-project/scripts/bear_avatar.b64', 'w').write(b64)
print('jpg bytes:', len(open(out_jpg, 'rb').read()), 'b64 chars:', len(b64))
