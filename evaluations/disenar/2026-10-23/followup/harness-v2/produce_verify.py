from pathlib import Path
import json, hashlib, xml.etree.ElementTree as ET
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageChops

p = Path(__file__).resolve().parent
brief = {'prompt': 'Diseña un icono original monocromo para esta app, legible a 24 px; entrega maestro vectorial y versiones negra y blanca.', 'app': 'Pliego', 'use': 'Guardar y volver a leer pasajes de libros; icono de app y marcador junto a su nombre.', 'constraints': ['sin iconografía ni paletas de otras marcas del usuario', 'negro/blanco y SVG editable', 'tamaño objetivo 24 px', 'originalidad de construcción, sin afirmar exclusividad marcaria ni reconocimiento medido'], 'concept': 'Hoja plegada con una franja recortada que marca el pasaje: silueta de página, esquina doblada y una sola línea interior.'}
(p/'brief.json').write_text(json.dumps(brief, ensure_ascii=False, indent=2)+'\n')
geometry = 'M5 3H14L20 9V21H5V3ZM7 5V19H18V10H13V5H7ZM15 6.4V8H16.6L15 6.4ZM9 13H16V15H9V13Z'

def render(svg, target, size):
    # MuPDF's SVG importer produces vector display lists before rasterization.
    with fitz.open(stream=svg.encode(), filetype='svg') as doc:
        doc[0].get_pixmap(matrix=fitz.Matrix(size/24, size/24), alpha=True).save(target)

for name, color in [('master', 'currentColor'), ('black', '#000000'), ('white', '#ffffff')]:
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" role="img" aria-labelledby="title"><title id="title">Pliego — pasaje guardado</title><path fill="{color}" fill-rule="evenodd" d="{geometry}"/></svg>\n'
    (p/f'pliego-{name}.svg').write_text(svg)
    for size in [16, 24, 48, 192]:
        render(svg, p/f'pliego-{name}-{size}.png', size)

font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
im = Image.new('RGB', (1000, 460), '#ececec')
draw = ImageDraw.Draw(im)
font = ImageFont.truetype(font_path, 22)
small = ImageFont.truetype(font_path, 15)
draw.text((32, 22), 'PLIEGO · prueba vectorial', font=font, fill='#222222')
for col, (variant, bg, fg) in enumerate([('black', 'white', 'black'), ('white', '#161616', 'white')]):
    x = 32+col*480
    draw.rectangle((x,72,x+456,410), fill=bg)
    draw.text((x+18,86), variant.upper(), font=small, fill=fg)
    for j, size in enumerate([16,24,48]):
        icon=Image.open(p/f'pliego-{variant}-{size}.png')
        px,py=x+28+j*95,160
        im.paste(icon,(px,py),icon)
        draw.text((px,226),f'{size} px · 1:1',font=small,fill=fg)
    icon=Image.open(p/f'pliego-{variant}-24.png').resize((120,120),Image.Resampling.NEAREST)
    im.paste(icon,(x+310,150),icon)
    draw.text((x+310,284),'24 px ×5',font=small,fill=fg)
    draw.text((x+18,355),'Guardar un pasaje',font=font,fill=fg)
im.save(p/'contact-sheet.png')
files=[]
for name in ['master','black','white']:
    target=p/f'pliego-{name}.svg'
    root=ET.parse(target).getroot()
    assert root.attrib['viewBox']=='0 0 24 24'
    assert not root.findall('.//{*}image')
    assert not root.findall('.//{*}script')
    assert len(root.findall('.//{*}path'))==1
    expected_fill = {'master': 'currentColor', 'black': '#000000', 'white': '#ffffff'}[name]
    actual_fill = root.find('.//{*}path').get('fill')
    assert actual_fill == expected_fill, (name, expected_fill, actual_fill)
    files.append({'path':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'vector_paths':1,'raster_images':0,'viewBox':root.attrib['viewBox']})
a=Image.open(p/'pliego-black-24.png').getchannel('A')
b=Image.open(p/'pliego-white-24.png').getchannel('A')
assert ImageChops.difference(a,b).getbbox() is None
svg=(p/'pliego-black.svg').read_text().replace('M9 13H16V15H9V13Z','M8 13H16V15H8V13Z')
(p/'edit-probe.svg').write_text(svg)
render(svg,p/'edit-probe.png',24)
edited_alpha=Image.open(p/'edit-probe.png').getchannel('A')
assert ImageChops.difference(a,edited_alpha).getbbox() is not None
(p/'checks.json').write_text(json.dumps({'status':'PASS','checks':['SVG real sin imágenes incrustadas','viewBox y tamaño objetivo 24','maestro currentColor y variantes negra/blanca','canal alfa idéntico entre variantes','edición de geometría y rerender produce cambio real'],'files':files,'renderer':'MuPDF via PyMuPDF '+fitz.VersionBind,'not_run':['reconocimiento con personas','exclusividad de marca','navegador nativo; bloqueo reportado por separado'],'visual_review':'PENDING'},ensure_ascii=False,indent=2)+'\n')
print('SVG structure, alpha consistency and editability: PASS')
