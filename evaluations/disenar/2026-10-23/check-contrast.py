"""Reproduce CLI boundary checks against a supplied disenar package."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--skill', required=True, type=Path)
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
script = args.skill / 'scripts/contrast.py'
cases = [
    ('black_white', ['#000000', '#ffffff'], 0, 21.0),
    ('reverse', ['#ffffff', '#000000'], 0, 21.0),
    ('equal', ['#123456', '#123456'], 1, 1.0),
    ('shorthand', ['#000', '#FFF'], 0, 21.0),
    ('above_boundary', ['#767676', '#ffffff'], 0, None),
    ('below_boundary', ['#777777', '#ffffff'], 1, None),
    ('threshold_custom', ['#777777', '#ffffff', '--threshold', '3'], 0, None),
    ('reject_alpha', ['#00000080', '#ffffff'], 2, None),
    ('reject_missing_hash', ['000000', '#ffffff'], 2, None),
    ('reject_nan', ['#000', '#fff', '--threshold', 'nan'], 2, None),
    ('reject_infinity', ['#000', '#fff', '--threshold', 'inf'], 2, None),
    ('reject_threshold_range', ['#000', '#fff', '--threshold', '22'], 2, None),
]
results = []
for name, values, expected_code, expected_ratio in cases:
    run = subprocess.run([sys.executable, str(script), *values], text=True, capture_output=True)
    data = json.loads(run.stdout) if run.stdout else None
    checks = [run.returncode == expected_code]
    if data is not None:
        checks.append(data['status'] == ('PASS' if expected_code == 0 else 'FAIL'))
        if expected_ratio is not None:
            checks.append(abs(data['ratio'] - expected_ratio) < 1e-12)
        if name == 'above_boundary':
            checks.append(4.5 < data['ratio'] < 4.6)
        if name == 'below_boundary':
            checks.append(4.4 < data['ratio'] < 4.5)
    results.append({'id': name, 'args': values, 'expected_exit': expected_code,
                    'actual_exit': run.returncode, 'output': data, 'stderr': run.stderr,
                    'status': 'PASS' if all(checks) else 'FAIL'})
report = {'candidate_script_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
          'method': 'Actual CLI invocations, boundary values and invalid input; no browser or full accessibility test',
          'cases': results}
args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'cases': len(results), 'passed': sum(x['status'] == 'PASS' for x in results)}))
raise SystemExit(0 if all(x['status'] == 'PASS' for x in results) else 1)
