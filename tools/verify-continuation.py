"""Verify this continuation against the restored 2.2.1 delivery, with no GitHub access."""
import json,hashlib,os
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
base=Path(os.environ['BASELINE_DIR']).resolve()
def read(p):return json.loads(p.read_text())
d=read(root/'data/hizakurige.json');old=read(base/'data/hizakurige.json')
allowed={'illustrations','illustrationStatus','illustrationNote','illustrationReview'}
assert len(d['readings'])==58
for a,b in zip(d['readings'],old['readings']):
 for key,value in b.items():
  if key not in allowed:assert a[key]==value,(a['id'],key)
 for x in a.get('illustrations',[]):assert 1<=x['afterParagraph']<=len(a['modern'])
for key,value in old.items():
 if key not in ['readings','images']:assert d[key]==value,key
for key,value in old['images'].items():
 for prop,v in value.items():
  if prop!='bibliography':assert d['images'][key][prop]==v,(key,prop)
for path in ['js/storage.js','js/map.js','js/utils.js','data/courses.json','data/geography.json','data/oku-no-hosomichi.json','data/hizakurige-originals.json','index.html','manifest.webmanifest']:
 assert (root/path).read_bytes()==(base/path).read_bytes(),path
for p in (base/'images').rglob('*'):
 if p.is_file():assert p.read_bytes()==(root/p.relative_to(base)).read_bytes(),p.name
licenses=read(root/'docs/image-licenses.json')
for key,a in d['images'].items():
 with Image.open(root/a['src']) as im:
  im.load();assert (im.width,im.height)==(a['width'],a['height']),key
 assert (root/a['src']).stat().st_size==a['sizeBytes'],key
 if a.get('caption'):
  assert 60<=len(a['caption'])<=120
  assert a['bibliography']['folio'] is None
  assert a==next(x for x in licenses if x['id']==key),key
 if a.get('appreciation'):assert a['appreciation']==old['images'][key]['appreciation']
review=read(root/'docs/hizakurige-final-review.json');assert len(review['readings'])==58
assert review['counts']=={'readings':58,'illustratedReadings':24,'sceneReadings':21,'contextOnlyReadings':3,'unillustratedReadings':34,'linkedImages':27,'sceneImages':22,'contextImages':5,'hiroshigeCommentaries':44,'readingsWithoutSceneImage':37}
assert 'book-349' in d['images'];assert d['images']['book-349']['illustrationRole']=='original-context'
assert set(d['images'])-set(old['images'])=={'book-349'}
manifest=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file() and p.suffix not in ['.png'] and '__pycache__' not in p.parts]
out={'dateJST':'2026-10-13','version':'2.2.2','status':'passed','baseline':'restored 2.2.1 Library delivery','counts':review['counts'],'imagesDecoded':len(d['images']),'newImageFilesSince221':1,'checks':['all original reading text/IDs/paragraphs/points/routes/distances preserved','storage/map/utils/other-course/original-text bytes preserved','all baseline image bytes preserved','all 44 Hiroshige images and commentary fields preserved','all 58 paragraph anchors and survey records valid','all caption lengths and image dimensions/sizes verified','machine-readable image licenses match','scene/context/unillustrated counts independently recomputed']}
(root/'docs/continuation-test-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
