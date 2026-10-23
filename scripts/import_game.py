"""Import a built game checkout as static files; no game backend is deployed."""
from pathlib import Path
import argparse
import shutil
import subprocess
import json

parser = argparse.ArgumentParser()
parser.add_argument('source', type=Path)
args = parser.parse_args()
source = args.source.resolve()
target = Path(__file__).resolve().parents[1] / 'gaming/golden-orbital-defense'
required = ['index.html', 'style.css', 'game.js', 'THIRD_PARTY.md', 'assets/THREE-LICENSE.txt']
for name in required:
    if not (source / name).is_file(): raise SystemExit(f'Missing game file: {name}')
for name in required:
    destination = target / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / name, destination)
# NASA spacecraft models and the Draco decoder they need (loaded at runtime).
for folder in ['assets/models', 'assets/draco']:
    src = source / folder
    if src.is_dir():
        dst = target / folder
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
html = (target / 'index.html').read_text(encoding='utf-8')
html = html.replace('</head>', '<link rel="canonical" href="https://goldstarorbital.com/gaming/golden-orbital-defense/">\n<meta name="description" content="Launch from Earth, fight your way to Mars, and protect your colony in Golden Orbital Defense, a free browser space game.">\n</head>')
html = html.replace('<button id="restart"', '<a class="website-return" href="/gaming/">← Back to Gaming</a>\n<button id="restart"')
if 'website-return' not in html:
    raise SystemExit('Game menu changed: update the Back to Gaming insertion.')
(target / 'index.html').write_text(html, encoding='utf-8')
with (target / 'style.css').open('a', encoding='utf-8') as css:
    css.write('\n.website-return { display:block; margin:12px 0; padding:12px; color:#e4c68c; text-align:center; font:12px monospace; }\n')
commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
(target / 'release.json').write_text(json.dumps({'repository':'GoldstarOrbital/golden-orbital-defense','commit':commit}, indent=2)+'\n', encoding='utf-8')
print(f'Imported game {commit} to {target}')
