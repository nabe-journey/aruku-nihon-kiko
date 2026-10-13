"""Verify IDs, text, routes, existing image bytes and new asset metadata against the baseline."""
import hashlib,json,pathlib,subprocess
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[1]
def original(file):return subprocess.check_output(['git','show','a5e108f8755ea0ae5f7440b89f63055b46b91cab:'+file],cwd=root)
d=json.loads((root/'data/hizakurige.json').read_text());old=json.loads(original('data/hizakurige.json'))
for key,value in old.items():
 if key not in ['readings','images','sources']:assert d[key]==value,key
assert len(d['readings'])==len(old['readings'])==58
for r,before in zip(d['readings'],old['readings']):
 for key,value in before.items():assert r[key]==value,(r['id'],key)
 assert r['illustrationReview']['status']=='reviewed';assert r['illustrationReview']['decisionReason'];
 for a in r.get('illustrations',[]):assert 1<=a['afterParagraph']<=len(r['modern'])
assert d['sources'][:len(old['sources'])]==old['sources']
for file in ['js/storage.js','js/map.js','data/courses.json','data/geography.json','data/oku-no-hosomichi.json','data/hizakurige-originals.json']:
 assert (root/file).read_bytes()==original(file),file
for file in subprocess.check_output(['git','ls-tree','-r','--name-only','a5e108f8755ea0ae5f7440b89f63055b46b91cab','images'],cwd=root,text=True).splitlines():
 assert hashlib.sha256((root/file).read_bytes()).digest()==hashlib.sha256(original(file)).digest(),file
for key,a in old['images'].items():
 for prop,value in a.items():
  if key!='book-71':assert d['images'][key][prop]==value,(key,prop)
licenses=json.loads((root/'docs/image-licenses.json').read_text());counts={'readings':58,'illustratedReadings':0,'linkedOriginalImages':0,'sceneIllustrations':0,'originalContextIllustrations':0,'reviewedReadings':58,'readingsWithoutLinkedImage':0,'newImageFiles':len(d['images'])-len(old['images']),'hiroshigeCommentaries':0}
for r in d['readings']:
 counts['illustratedReadings']+=bool(r.get('illustrations'));counts['linkedOriginalImages']+=len(r.get('illustrations',[]));counts['readingsWithoutLinkedImage']+=not bool(r.get('illustrations'))
for key,a in d['images'].items():
 with Image.open(root/a['src']) as im:
  im.load();assert(im.width,im.height)==(a['width'],a['height']),key
 assert (root/a['src']).stat().st_size==a['sizeBytes'],key
 if a.get('caption'):
  assert 60<=len(a['caption'])<=120;assert a.get('bibliography',{}).get('canvas');assert a['bibliography'].get('alternateWitness');counts['sceneIllustrations']+=a['illustrationRole']=='scene';counts['originalContextIllustrations']+=a['illustrationRole']=='original-context'
 if a.get('appreciation'):assert 200<=len(a['appreciation'])<=400;counts['hiroshigeCommentaries']+=1
 if a.get('caption') or a.get('appreciation'):assert a==next(x for x in licenses if x['id']==key),key
out={'date':'2026-10-13','status':'passed','baseline':'a5e108f8755ea0ae5f7440b89f63055b46b91cab','counts':counts,'checks':['all original reading fields unchanged','route/IDs/distances unchanged','storage/map/other-course/original text bytes unchanged','all previously tracked image bytes unchanged','all image bytes/dimensions/sizes verified','paragraph anchors valid','caption/commentary length ranges met','machine-readable licenses agree']}
(root/'docs/hizakurige-data-test-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
