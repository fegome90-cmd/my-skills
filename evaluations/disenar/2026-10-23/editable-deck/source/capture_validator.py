#!/usr/bin/env python3
"""Run one validator and atomically preserve its execution and JSON result."""
from pathlib import Path
import json
import os
import shlex
import subprocess
import sys

if len(sys.argv) < 4 or sys.argv[2] != '--':
    raise SystemExit('Usage: capture_validator.py OUTPUT_JSON -- COMMAND [ARG ...]')

output = Path(sys.argv[1]).resolve()
command = sys.argv[3:]
record = {
    'status': 'BLOCKED',
    'command': command,
    'command_display': shlex.join(command),
    'cwd': str(Path.cwd()),
    'exit_code': None,
    'stdout': '',
    'stderr': '',
    'report': None,
}
try:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120, check=False)
    record.update(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
    if not result.stdout.strip():
        record['reason'] = 'The validator produced no JSON report on stdout.'
    else:
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            record['reason'] = f'The validator stdout is not valid JSON: {error}'
        else:
            record['report'] = report
            if not isinstance(report, dict) or 'finding_count' not in report or 'findings' not in report:
                record['reason'] = 'The JSON report does not contain the expected result fields.'
            elif result.returncode == 0 and report['finding_count'] == 0 and report['findings'] == []:
                record['status'] = 'PASS'
                record['reason'] = 'Validator returned zero and reported no findings.'
            else:
                record['status'] = 'FAIL'
                record['reason'] = 'Validator returned nonzero or reported findings.'
except subprocess.TimeoutExpired as error:
    record['reason'] = 'The validator exceeded the 120-second timeout.'
    record['stdout'] = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or '')
    record['stderr'] = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or '')
except OSError as error:
    record['reason'] = f'The validator could not execute: {error}'

output.parent.mkdir(parents=True, exist_ok=True)
temporary = output.with_suffix(output.suffix + '.tmp')
temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
os.replace(temporary, output)
print(json.dumps({'status': record['status'], 'exit_code': record['exit_code'], 'record': str(output), 'reason': record['reason']}, ensure_ascii=False))
raise SystemExit(0 if record['status'] == 'PASS' else 2)
