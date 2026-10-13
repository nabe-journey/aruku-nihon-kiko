"""Package the local update and research checkpoint without committing or pushing."""
import hashlib,json,pathlib,subprocess,tarfile,io,tempfile,zipfile
root=pathlib.Path(__file__).resolve().parents[1];workspace=root.parent;output=workspace/'deliverables';output.mkdir(exist_ok=True)
baseline='a5e108f8755ea0ae5f7440b89f63055b46b91cab'
def git(*args):return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.PIPE)
changed=git('diff','--name-only',baseline).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()
internal={'docs/reader-mobile.png','docs/hiroshige-mobile.png'}
changed=sorted(set(changed)-{'docs/update-file-manifest.json'}-internal)
files=[]
for file in changed:
 p=root/file
 try:before=git('show',baseline+':'+file)
 except subprocess.CalledProcessError:before=None
 files.append({'path':file,'sizeBytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'baselineSha256':hashlib.sha256(before).hexdigest() if before else None})
(root/'docs/update-file-manifest.json').write_text(json.dumps({'baseline':baseline,'files':files},ensure_ascii=False,indent=2)+'\n')
changed.append('docs/update-file-manifest.json')
patch=git('diff','--binary',baseline)
for file in git('ls-files','--others','--exclude-standard').decode().splitlines():
 if file in internal:continue
 r=subprocess.run(['git','diff','--no-index','--binary','--','/dev/null',file],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if r.returncode not in [0,1]:raise RuntimeError(r.stderr.decode())
 patch+=r.stdout
patchfile=output/'aruku-nihon-kiko-changes-20261013.patch';patchfile.write_bytes(patch)
with tempfile.TemporaryDirectory(prefix='hiza-apply-') as temp:
 target=pathlib.Path(temp);archive=git('archive',baseline)
 with tarfile.open(fileobj=io.BytesIO(archive)) as t:t.extractall(target,filter='data')
 subprocess.run(['git','apply','--check',str(patchfile)],cwd=target,check=True)
 subprocess.run(['git','apply',str(patchfile)],cwd=target,check=True)
 for file in changed:assert (target/file).read_bytes()==(root/file).read_bytes(),file
print('patch apply verified',len(changed),'files')
zipfileapp=output/'aruku-nihon-kiko-update-20261013.zip'
with zipfile.ZipFile(zipfileapp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file() and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.parts and p.relative_to(root).as_posix() not in internal:z.write(p,str(pathlib.Path(root.name)/p.relative_to(root)))
research=workspace/'research';checkpoint=output/'aruku-nihon-kiko-research-checkpoint-20261013.zip'
with zipfile.ZipFile(checkpoint,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 z.write(root/'docs/RESUME.md','RESUME.md');z.write(root/'docs/UPDATE_REPORT.md','UPDATE_REPORT.md');z.write(root/'docs/HIZAKURIGE_ILLUSTRATION_AUDIT.md','HIZAKURIGE_ILLUSTRATION_AUDIT.md')
 for p in sorted(research.rglob('*')):
  rel=p.relative_to(research)
  if p.is_file() and 'thumbs' not in rel.parts and p.suffix in ['.jpg','.json','.txt','.py','.html'] and not ('waseda' in rel.parts and p.suffix=='.jpg'):z.write(p,str(pathlib.Path('research')/rel))
for p in [zipfileapp,checkpoint,patchfile]:print(p.name,p.stat().st_size)
