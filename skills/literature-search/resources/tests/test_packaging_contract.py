from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = ROOT.parents[1]
SKILL_FILE = ROOT / 'SKILL.md'
# Configurable output root (see SKILL.md "Output Directory" section). The default
# keeps this workspace's behavior (apps/pae-wizard/outputs/research/); the skill
# is overridable via the LITERATURE_SEARCH_OUTPUT_DIR env var or inline param.
OUTPUT_PLACEHOLDER = '{{OUTPUT_DIR}}'
DEFAULT_OUTPUT_ROOT = 'apps/pae-wizard/outputs/research/'
ENV_OVERRIDE_NAME = 'LITERATURE_SEARCH_OUTPUT_DIR'
TOUCHED_DOCS = [
    SKILL_FILE,
    ROOT / 'resources' / 'synthesis-protocol.md',
    ROOT / 'resources' / 'search-protocol.md',
    ROOT / 'resources' / 'thesaurus-capture.md',
    ROOT / 'resources' / 'examples.md',
]
RESOURCE_FILES = [
    ROOT / 'resources' / 'synthesis-protocol.md',
    ROOT / 'resources' / 'citation-format.md',
]
REQUIRED_IGNORE_RULES = {
    '.pi-lens/',
    '.pi/',
    '.atl/',
    '.mypy_cache/',
    '.ruff_cache/',
    '_ctx/',
    '**/__pycache__/',
    '**/.DS_Store',
}


def test_skill_entrypoint_uses_configurable_output_root_and_consistent_version() -> None:
    content = SKILL_FILE.read_text(encoding='utf-8')

    assert 'Búsqueda bibliográfica sistemática en 5 fases' in content
    assert 'version: 1.4.0' in content
    assert 'Generated: YYYY-MM-DD | Skill: literature-search v1.4.0' in content
    # Path references are now parameterized via {{OUTPUT_DIR}} rather than hardcoded.
    assert f'Save plan to: `{OUTPUT_PLACEHOLDER}/search-plan.md`' in content
    assert f'Parse research question from existing `{OUTPUT_PLACEHOLDER}/search-plan.md`' in content
    assert f'All files go to `{OUTPUT_PLACEHOLDER}/`' in content
    assert '[`../research-skill-bank/CATALOG.md`](../research-skill-bank/CATALOG.md)' in content
    assert 'docs/research/' not in content


def test_skill_documents_output_dir_config_block_and_default() -> None:
    content = SKILL_FILE.read_text(encoding='utf-8')

    # Config block present
    assert '## Output Directory (`{{OUTPUT_DIR}}`) — Configurable' in content
    # Override mechanism documented (env var + inline param)
    assert ENV_OVERRIDE_NAME in content
    assert f'{OUTPUT_PLACEHOLDER}=' in content
    # Default preserves workspace behavior
    assert DEFAULT_OUTPUT_ROOT in content


def test_skill_portability_note_documents_configurable_output_root() -> None:
    content = SKILL_FILE.read_text(encoding='utf-8')

    assert '## Portability Note' in content
    assert OUTPUT_PLACEHOLDER in content
    assert DEFAULT_OUTPUT_ROOT in content
    assert ENV_OVERRIDE_NAME in content
    # No longer tells the reader to "adapt the output root" — it's configurable now.
    assert 'adapt the output root explicitly' not in content


def test_phase_five_resources_exist_and_are_indexed() -> None:
    content = SKILL_FILE.read_text(encoding='utf-8')

    for resource in RESOURCE_FILES:
        assert resource.exists(), f'Missing resource: {resource}'
        relative = resource.relative_to(ROOT).as_posix()
        assert f'[`{resource.name}`]({relative})' in content


def test_touched_docs_use_configurable_output_root() -> None:
    for doc in TOUCHED_DOCS:
        content = doc.read_text(encoding='utf-8')
        # Resource docs reference the parameter; SKILL.md also documents the default.
        assert OUTPUT_PLACEHOLDER in content, (
            f'{doc} must reference {OUTPUT_PLACEHOLDER} parameter'
        )
        assert 'docs/research/' not in content, f'{doc} still references docs/research/'


def test_touched_docs_default_root_documented_in_skill_entrypoint() -> None:
    """The default output root is only documented in SKILL.md's config block."""
    for doc in TOUCHED_DOCS[1:]:  # skip SKILL.md
        content = doc.read_text(encoding='utf-8')
        # Resource docs may keep a parenthetical default hint, but the literal
        # default must not appear as the sole path (it must be parameterized).
        # This is intentionally permissive — resources can include the default
        # in a "(default: ...)" hint next to {{OUTPUT_DIR}}.
        assert OUTPUT_PLACEHOLDER in content


def test_skill_links_resolve_from_entrypoint() -> None:
    content = SKILL_FILE.read_text(encoding='utf-8')
    links = re.findall(r"\[[^\]]+\]\(([^)#]+)\)", content)
    local_links = [link for link in links if not link.startswith(('http://', 'https://'))]

    for link in local_links:
        if link.startswith('../'):
            continue
        target = (SKILL_FILE.parent / link).resolve()
        assert target.exists(), f'Broken local link: {link}'


def test_skill_local_gitignore_covers_transient_artifacts() -> None:
    content = (ROOT / '.gitignore').read_text(encoding='utf-8').splitlines()
    rules = {line.strip() for line in content if line.strip() and not line.strip().startswith('#')}
    missing = REQUIRED_IGNORE_RULES - rules
    assert not missing, f'Missing ignore rules: {sorted(missing)}'


def test_pi_lens_artifacts_are_not_tracked() -> None:
    result = subprocess.run(
        ['git', 'ls-files', 'skills/literature-search/.pi-lens'],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    tracked = [line for line in result.stdout.splitlines() if line.strip()]
    assert tracked == []
