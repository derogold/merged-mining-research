#!/usr/bin/env python3
"""Verify preserved experiment bytes and newly authored Markdown links."""
import hashlib,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'evidence-manifest.json').read_text())
errors=[]
for row in manifest:
 p=root/row['path']
 if not p.is_file() or p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
  errors.append('Evidence mismatch: '+row['path'])
actual={str(p.relative_to(root)) for p in (root/'experiments').rglob('*') if p.is_file()}
expected={r['path'] for r in manifest}
if actual!=expected:errors.append('Unmanifested or missing evidence paths: '+repr(actual^expected))
links=0
for p in [root/'README.md',*sorted((root/'docs').glob('*.md'))]:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  links+=1
  if not (p.parent/target.split('#')[0]).exists():errors.append(f'Broken link: {p.name}: {target}')
print(json.dumps({'evidence_files':len(manifest),'local_links_checked':links,'errors':errors},indent=2))
raise SystemExit(bool(errors))
