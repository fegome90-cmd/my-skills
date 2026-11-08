"""Exercise the verifier CLIs with valid fixtures and deliberate defects."""
import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import traceback
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--revision', choices=['original', 'fixed'], required=True)
parser.add_argument('--archive', type=Path, default=HERE.parent / 'evidence.zip')
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
contract = json.loads((HERE / 'contract.json').read_text())
results = []


@contextmanager
def fixture():
    with tempfile.TemporaryDirectory(prefix='disenar-oracle-') as directory:
        root = Path(directory)
        with ZipFile(args.archive) as archive:
            for member in archive.infolist():
                path = PurePosixPath(member.filename)
                if path.is_absolute() or '..' in path.parts or (member.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('Unsafe archive member')
            archive.extractall(root)
        manifest = json.loads((root / 'BUNDLE_MANIFEST.json').read_text())
        for row in manifest['files']:
            assert hashlib.sha256((root / row['path']).read_bytes()).hexdigest() == row['sha256']
        if args.revision == 'fixed':
            for row in contract['files']:
                target = root / row['target']
                assert hashlib.sha256(target.read_bytes()).hexdigest() == row['original_sha256']
                target.write_bytes((HERE.parent / row['source']).read_bytes())
        yield root


def run(path, *arguments):
    command = [sys.executable, str(path), *map(str, arguments)]
    process = subprocess.run(command, capture_output=True, text=True, timeout=30)
    current['commands'].append({'command': command, 'exit_code': process.returncode,
                                'stdout': process.stdout, 'stderr': process.stderr})
    return process


def replace_once(path, before, after):
    source = path.read_text()
    assert source.count(before) == 1, (path, before)
    path.write_text(source.replace(before, after, 1))


def contrast_valid(root):
    result = run(root / 'followup/bank/checks-contrast.py')
    assert result.returncode == 0
    rows = json.loads(result.stdout)
    assert [row['pairs'] for row in rows] == [12, 9]
    assert all(row['failures'] == [] for row in rows)


def contrast_invalid(root):
    script = root / 'followup/bank/checks-contrast.py'
    replace_once(script, "('Tinta claro', '#0e0e0d','#f4f4f0',4.5)",
                 "('Tinta claro', '#f4f4f0','#f4f4f0',4.5)")
    result = run(script)
    rows = json.loads(result.stdout)
    failure = rows[0]['failures'][0]
    assert failure['ratio'] == 1.0 and failure['threshold'] == 4.5 and failure['status'] == 'FAIL'
    assert result.returncode == 1, 'A reported contrast failure must fail the CLI'


def svg_valid(root):
    result = run(root / 'followup/identity/produce_verify.py')
    assert result.returncode == 0, result.stderr
    report = json.loads((root / 'followup/identity/checks.json').read_text())
    assert report['status'] == 'PASS' and report['visual_review'] == 'PENDING'


def svg_invalid_white(root):
    script = root / 'followup/identity/produce_verify.py'
    replace_once(script, "('white', '#ffffff')", "('white', '#000000')")
    result = run(script)
    assert result.returncode != 0, 'A black white variant must be rejected'
    assert 'white' in result.stderr and '#ffffff' in result.stderr


def pptx_valid_boundary(root):
    validator = root / 'editable-deck/source/validate_deck.py'
    native = root / 'editable-deck/output/plan-talleres-2027.pptx'
    assert not (root / 'editable-deck/checks').exists()
    control = run(validator, native)
    assert control.returncode == 0, control.stderr
    assert json.loads(control.stdout)['status'] == 'PASS'
    probe = run(root / 'followup/pptx_raster_probe.py')
    assert probe.returncode == 0, probe.stderr
    report = json.loads((root / 'followup/pptx-raster/results.json').read_text())
    assert report['native_validator']['exit_code'] == 0
    assert report['negative_validator']['exit_code'] == 1
    assert report['negative_validator']['result']['code'] == 'NATIVE_TEXT_MISSING'
    assert report['negative_validator']['result']['sha256'] == report['image_only']['sha256']


def pptx_broken_validator(root):
    validator = root / 'editable-deck/source/validate_deck.py'
    validator.write_text('raise RuntimeError("ORACLE_TEST_VALIDATOR_UNAVAILABLE")\n')
    result = run(root / 'followup/pptx_raster_probe.py')
    assert result.returncode != 0, 'A validator crash must not satisfy the negative case'
    assert '"probe_status": "PASS"' not in result.stdout


def pptx_negative_operational_error(root):
    validator = root / 'editable-deck/source/validate_deck.py'
    validator.write_text('import sys\nif "raster-only" in sys.argv[1]:\n    raise RuntimeError("ORACLE_TEST_RASTER_CRASH")\n' + validator.read_text())
    (root / 'editable-deck/checks').mkdir(exist_ok=True)
    native = root / 'editable-deck/output/plan-talleres-2027.pptx'
    control = run(validator, native)
    assert control.returncode == 0, control.stderr
    result = run(root / 'followup/pptx_raster_probe.py')
    assert result.returncode != 0, 'An operational failure on raster must not count as a semantic rejection'
    assert '"probe_status": "PASS"' not in result.stdout


checks = [
    ('contrast-valid', contrast_valid), ('contrast-invalid', contrast_invalid),
    ('svg-valid', svg_valid), ('svg-invalid-white', svg_invalid_white),
    ('pptx-valid-boundary', pptx_valid_boundary),
    ('pptx-broken-validator', pptx_broken_validator),
    ('pptx-negative-operational-error', pptx_negative_operational_error),
]
for check_id, check in checks:
    current = {'id': check_id, 'commands': []}
    try:
        with fixture() as root:
            check(root)
        current['status'] = 'PASS'
    except Exception as error:
        current['status'] = 'FAIL'
        current['error'] = str(error)
        current['traceback'] = traceback.format_exc()
    results.append(current)

report = {
    'revision': args.revision, 'source_commit': contract['source_commit'],
    'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
    'contract_sha256': hashlib.sha256((HERE / 'contract.json').read_bytes()).hexdigest(),
    'test_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'checks': results,
    'totals': {status: sum(row['status'] == status for row in results) for status in ['PASS', 'FAIL']},
    'scope': 'Verifier regression controls. Does not test browser interaction, host activation or human outcomes.',
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report['totals']))
raise SystemExit(any(row['status'] == 'FAIL' for row in results))
