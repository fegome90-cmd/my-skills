"""Negative fixture for the previously unexercised image-only PPTX boundary.

Only mutates a test copy of the prior deck. The original and its evidence stay unchanged.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json, re, subprocess, sys
import xml.etree.ElementTree as ET

here = Path(__file__).resolve().parent
baseline = here.parent/'editable-deck'
original = baseline/'output/plan-talleres-2027.pptx'
dest = here/'pptx-raster'
dest.mkdir(exist_ok=True)
output = dest/'raster-only.pptx'
ns = {'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for prefix, uri in ns.items(): ET.register_namespace(prefix,uri)
rel_ns='http://schemas.openxmlformats.org/package/2006/relationships'
ct_ns='http://schemas.openxmlformats.org/package/2006/content-types'
with ZipFile(original) as source:
    contents={name:source.read(name) for name in source.namelist()}
    size=ET.fromstring(contents['ppt/presentation.xml']).find('p:sldSz',ns)
    cx,cy=size.get('cx'),size.get('cy')
    for i in range(1,9):
        key=f'ppt/slides/slide{i}.xml'
        root=ET.fromstring(contents[key])
        tree=root.find('.//p:spTree',ns)
        for child in list(tree):
            if child.tag not in {f'{{{ns["p"]}}}nvGrpSpPr',f'{{{ns["p"]}}}grpSpPr'}:
                tree.remove(child)
        picture=ET.fromstring(f'''<p:pic xmlns:p="{ns['p']}" xmlns:a="{ns['a']}" xmlns:r="{ns['r']}"><p:nvPicPr><p:cNvPr id="2" name="Image-only negative fixture"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="qaRaster"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>''')
        tree.append(picture)
        contents[key]=ET.tostring(root,encoding='utf-8',xml_declaration=True)
        rel_key=f'ppt/slides/_rels/slide{i}.xml.rels'
        rel=ET.fromstring(contents[rel_key])
        ET.SubElement(rel,f'{{{rel_ns}}}Relationship',{'Id':'qaRaster','Type':ns['r']+'/image','Target':f'../media/qa-raster-{i}.png'})
        contents[rel_key]=ET.tostring(rel,encoding='utf-8',xml_declaration=True)
        contents[f'ppt/media/qa-raster-{i}.png']=(baseline/f'renders/slide-{i:02d}.png').read_bytes()
    ct=ET.fromstring(contents['[Content_Types].xml'])
    if not any(x.get('Extension')=='png' for x in ct):
        ET.SubElement(ct,f'{{{ct_ns}}}Default',{'Extension':'png','ContentType':'image/png'})
    contents['[Content_Types].xml']=ET.tostring(ct,encoding='utf-8',xml_declaration=True)
with ZipFile(output,'w',ZIP_DEFLATED) as target:
    for name,data in contents.items(): target.writestr(name,data)

def inspect(path):
    slides=[]
    with ZipFile(path) as archive:
        for i in range(1,9):
            root=ET.fromstring(archive.read(f'ppt/slides/slide{i}.xml'))
            slides.append({'slide':i,'native_text_runs':len(root.findall('.//a:t',ns)),
                'pictures':len(root.findall('.//p:pic',ns)),
                'connectors':len(root.findall('.//p:cxnSp',ns))})
        notes=[x for x in archive.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',x)]
    return {'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'slides':slides,'notes':len(notes),
            'requested_editability': 'PASS' if all(x['native_text_runs']>0 for x in slides) and slides[2]['connectors']==2 else 'FAIL'}

native=inspect(original)
raster=inspect(output)
assert native['requested_editability']=='PASS'
assert raster['requested_editability']=='FAIL'
assert raster['notes']==8 and all(x['pictures']==1 for x in raster['slides'])
control=subprocess.run([sys.executable,str(baseline/'source/validate_deck.py'),str(original)],capture_output=True,text=True)
(dest/'existing-validator-positive.log').write_text(control.stdout+control.stderr)
assert control.returncode==0, ('native validator did not accept the control', control.stderr)
native_result=json.loads(control.stdout)
assert native_result['status']=='PASS' and native_result['sha256']==native['sha256']
check=subprocess.run([sys.executable,str(baseline/'source/validate_deck.py'),str(output)],capture_output=True,text=True)
(dest/'existing-validator-negative.log').write_text(check.stdout+check.stderr)
assert check.returncode==1, ('unexpected negative validator exit', check.returncode)
negative_result=json.loads(check.stdout)
assert negative_result['status']=='FAIL' and negative_result['code']=='NATIVE_TEXT_MISSING'
assert negative_result['sha256']==raster['sha256'] and negative_result['slide']==1
report={'probe_status':'PASS','native':native,'image_only':raster,
        'native_validator':{'exit_code':control.returncode,'result':native_result},
        'negative_validator':{'exit_code':check.returncode,'result':negative_result},
        'existing_validator_exit_code':check.returncode,
        'outcome':'Image-only exporter cannot satisfy requested text/diagram editability. Preserve output as partial and disclose exact unmet requirement; use native producer when available.',
        'scope':'Actual OOXML output rejection; no Microsoft PowerPoint UI or skill invocation claim.'}
(dest/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'probe_status':'PASS','native_editability':native['requested_editability'],'raster_editability':raster['requested_editability'],'negative_validator_exit':check.returncode}))
