// Publish istoriya-rossii.html as a static CodeSandbox (no account needed via define API).
const fs = require('fs');
const lz = require('lz-string');
const path = require('path');

const FILE = '/home/z/my-project/download/istoriya-rossii.html';
const html = fs.readFileSync(FILE, 'utf8');

const files = {
  'index.html': { content: html },
};

const parameters = lz.compressToBase64(JSON.stringify({ files }))
  .replace(/\+/g, '-')
  .replace(/\//g, '_')
  .replace(/=+$/, '');

(async () => {
  const res = await fetch('https://codesandbox.io/api/v1/sandboxes/define?json=1', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
    },
    body: 'parameters=' + encodeURIComponent(parameters),
  });
  const text = await res.text();
  console.log('HTTP', res.status);
  console.log(text.slice(0, 600));
  try {
    const j = JSON.parse(text);
    if (j.sandbox_id) {
      console.log('SANDBOX_ID=' + j.sandbox_id);
      console.log('EDITOR_URL=https://codesandbox.io/s/' + j.sandbox_id);
      console.log('PREVIEW_URL=https://' + j.sandbox_id + '.csb.app/');
    }
  } catch (e) {
    console.error('Not JSON:', e.message);
  }
})();
