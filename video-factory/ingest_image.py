import json, pathlib, sys, hashlib
from PIL import Image

root=pathlib.Path(__file__).resolve().parent
image_id=sys.argv[1]
index=int(sys.argv[2])
source=pathlib.Path(sys.argv[3])
assert image_id[:3] in {'RES','COA','LOC','CB-'} and image_id.replace('-','').isalnum()
assert index in (1,2,3)
assert source.is_file() and source.parent.name=='generated_images'
dst=root/'videos'/image_id/'images'
dst.mkdir(parents=True,exist_ok=True)
out=dst/f'{index:02d}.webp'
with Image.open(source) as im:
 im.convert('RGB').save(out,'WEBP',quality=92,method=6)
size=Image.open(out).size
meta={'id':image_id,'image_index':index,'relative_path':str(out.relative_to(root)),'source_generated':str(source),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'width':size[0],'height':size[1]}
(dst/f'{index:02d}.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out),'kb':out.stat().st_size//1024,'size':size}))
