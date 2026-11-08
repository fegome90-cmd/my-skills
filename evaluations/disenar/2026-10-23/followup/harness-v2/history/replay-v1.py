"""Replay bounded checks in a temporary extraction. No network or installation.

Full REA build reconstruction is separate; see bank/README.md in evidence.zip.
This never marks browser, host loading, human studies or physical print as passed.
"""
import argparse, hashlib, json, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

here=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--skill',type=Path,default=here.parents[3]/'skills/disenar')
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
candidate=args.skill.resolve()
if not (candidate/'SKILL.md').is_file():
    parser.error('--skill must identify a real candidate directory')

def inventory(path):
    return [{'path':str(p.relative_to(path)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(path.rglob('*')) if p.is_file()]

frozen=json.loads((here/'source-integrity.json').read_text())['inventory']
if inventory(candidate)!=frozen:
    parser.error('candidate bytes differ from the frozen revision')
before=inventory(candidate)
results=[]
with tempfile.TemporaryDirectory(prefix='disenar-replay-') as temp:
    temp=Path(temp)
    with ZipFile(here/'evidence.zip') as archive:
        for name in archive.namelist():
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts:
                raise ValueError('unsafe archive member')
        archive.extractall(temp)
    manifest=json.loads((temp/'BUNDLE_MANIFEST.json').read_text())
    for row in manifest['files']:
        assert hashlib.sha256((temp/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
    work=temp/'followup'
    commands=[
        ('vue-runtime', ['node',str(work/'vue/scripts/verify.mjs')]),
        ('vue-static', [sys.executable,str(work/'vue/scripts/verify-static.py'),'--skill',str(candidate)]),
        ('vue-react-compatibility', [sys.executable,str(work/'vue/scripts/check-compatibility.py')]),
        ('slide-state', ['node',str(work/'slides/evidence/test-state.cjs')]),
        ('sql', [sys.executable,str(work/'scope/sql/run.py')]),
        ('skill-audit', [sys.executable,str(work/'scope/audit/run.py'),'--candidate',str(candidate)]),
        ('svg-vector-edit', [sys.executable,str(work/'identity/produce_verify.py')]),
        ('pptx-raster-boundary', [sys.executable,str(work/'pptx_raster_probe.py')]),
        ('generic-source', ['bash',str(work/'bank/scripts/verify-generic.sh')]),
        ('bank-color-pairs', [sys.executable,str(work/'bank/checks-contrast.py')]),
    ]
    for check,command in commands:
        run=subprocess.run(command,cwd=work,text=True,capture_output=True)
        results.append({'id':check,'status':'PASS' if run.returncode==0 else 'FAIL','exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
after=inventory(candidate)
assert before==after,'replay changed candidate'
report={'purpose':'bounded replay, not global acceptance','archive_sha256':hashlib.sha256((here/'evidence.zip').read_bytes()).hexdigest(),'evaluator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'candidate_unchanged':before==after,'checks':results,'not_replayed':['full REA npm build/test (recorded logs and separate reconstruction instructions)','browser render, keyboard, timing and device tests','host installation or automatic invocation','human outcomes, physical printing or Microsoft Office UI']}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'PASS':sum(x['status']=='PASS' for x in results),'FAIL':sum(x['status']=='FAIL' for x in results),'candidate_unchanged':before==after}))
raise SystemExit(any(x['status']=='FAIL' for x in results))
