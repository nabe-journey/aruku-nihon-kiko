"""Create a full local delivery without Git operations; verify every archived byte."""
import hashlib,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root.parent/'deliverables';out.mkdir(exist_ok=True)
def included(p):return p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and not(p.parent==root/'docs' and p.suffix=='.png')
files=[p for p in sorted(root.rglob('*')) if included(p) and p.name!='package-integrity.json']
meta={'version':'2.2.2','dateJST':'2026-10-13','files':[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(root/'docs/package-integrity.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');files.append(root/'docs/package-integrity.json')
target=out/'aruku-nihon-kiko-2.2.2-complete.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,str(Path('aruku-nihon-kiko')/p.relative_to(root)))
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 for p in files:assert z.read(str(Path('aruku-nihon-kiko')/p.relative_to(root)))==p.read_bytes(),p.name
print(json.dumps({'file':str(target),'bytes':target.stat().st_size,'entries':len(files),'integrity':'all archived bytes match'},ensure_ascii=False))
