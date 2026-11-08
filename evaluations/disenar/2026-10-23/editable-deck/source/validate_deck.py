#!/usr/bin/env python3
"""Validate the requested native content and notes without third-party packages."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
PPTX = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'build/candidate.pptx'
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
EXPECTED = [
    ['Plan de talleres 2027:', 'aprender haciendo', 'equipo de 12 personas'],
    ['Objetivo', 'Alinear criterios', 'Producir un prototipo', 'compartido'],
    ['Tres etapas', 'Diagnóstico', 'Diseño', 'Prototipo', '2 sesiones', '3 sesiones'],
    ['Calendario', 'Semana 1', 'Diagnóstico', 'Semana 2', 'Diseño', 'Semanas 3 y 4', 'Prototipo'],
    ['Roles', 'Coordinación', 'Organiza', 'Facilitación', 'Guía', 'Participantes', 'Construyen'],
    ['Recursos', 'Sala', 'Equipo de proyección', 'Materiales de trabajo'],
    ['Riesgos y respuestas', 'Disponibilidad', 'Agendar con anticipación', 'Retrasos', 'Priorizar alcance', 'Dificultades técnicas', 'Preparar una alternativa sencilla'],
    ['Próxima decisión', 'Acordar fecha de inicio', 'y responsables'],
]
report = {'file': str(PPTX), 'sha256': hashlib.sha256(PPTX.read_bytes()).hexdigest(),
          'status': 'PASS', 'slides': [], 'checks': []}
with ZipFile(PPTX) as z:
    slide_names = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)),
                         key=lambda n: int(re.search(r'slide(\d+)', n).group(1)))
    note_names = sorted((n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)),
                        key=lambda n: int(re.search(r'notesSlide(\d+)', n).group(1)))
    assert len(slide_names) == 8, len(slide_names)
    assert len(note_names) == 8, len(note_names)
    for i, name in enumerate(slide_names):
        root = ET.fromstring(z.read(name))
        texts = [e.text or '' for e in root.findall('.//a:t', NS)]
        joined = ' '.join(texts)
        for expected in EXPECTED[i]:
            assert expected in joined, (i + 1, expected, joined)
        pictures = len(root.findall('.//p:pic', NS))
        raster_refs = len(root.findall('.//a:blip', NS))
        assert pictures == 0 and raster_refs == 0, (name, 'rasterized content')
        shapes = root.findall('.//p:spTree/p:sp', NS)
        connectors = root.findall('.//p:spTree/p:cxnSp', NS)
        text_shapes = [s for s in shapes if s.findall('.//a:t', NS)]
        assert len(text_shapes) > 0
        if i == 2:
            stages = []
            for s in shapes:
                nv = s.find('p:nvSpPr/p:cNvPr', NS)
                if nv is not None and nv.get('name', '').startswith('etapa-'):
                    stages.append(s)
            assert len(stages) == 3
            assert len(connectors) == 2
            stage_ids = {s.find('p:nvSpPr/p:cNvPr', NS).get('id') for s in stages}
            for c in connectors:
                start = c.find('.//a:stCxn', NS)
                end = c.find('.//a:endCxn', NS)
                assert start is not None and end is not None
                assert start.get('id') in stage_ids and end.get('id') in stage_ids
            assert texts.count('2 sesiones') == 2 and texts.count('3 sesiones') == 1
        note = ET.fromstring(z.read(note_names[i]))
        note_text = ' '.join(e.text or '' for e in note.findall('.//a:t', NS))
        assert 'Tiempo sugerido:' in note_text and 'Transición:' in note_text
        assert len(note_text) > 300
        report['slides'].append({'number': i + 1, 'text': texts, 'native_shapes': len(shapes),
                                  'native_text_shapes': len(text_shapes), 'native_connectors': len(connectors),
                                  'pictures': pictures, 'notes_words': len(note_text.split())})
    report['checks'] = [
        {'criterion': 'Exactly 8 slides and 8 non-empty notes parts', 'status': 'PASS'},
        {'criterion': 'Required content in the requested slide order', 'status': 'PASS'},
        {'criterion': 'Native text objects without picture replacement', 'status': 'PASS'},
        {'criterion': 'Three native process nodes and two attached native connectors', 'status': 'PASS'},
    ]
notes = json.loads((ROOT / 'source/notes.json').read_text())
report['suggested_duration_seconds'] = sum(n['seconds'] for n in notes)
report['spoken_notes_words'] = sum(len(n['talk'].split()) for n in notes)
assert report['suggested_duration_seconds'] == 300
report['claim_boundary'] = 'OOXML package inspection. Does not verify interactive editing in Microsoft PowerPoint or actual speaking time.'
out = ROOT / 'checks/content-editability.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps({key: report[key] for key in ['status', 'file', 'sha256', 'suggested_duration_seconds', 'spoken_notes_words']}, ensure_ascii=False, indent=2))
