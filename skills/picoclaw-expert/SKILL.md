---
name: picoclaw-expert
description: "Expert knowledge for PicoClaw system - debugging, extending, and maintaining the hardened AI study assistant."
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
---

# PicoClaw Expert

Specialized knowledge for working with PicoClaw - the hardened AI study assistant for EEO-2025 exam preparation.

## When to Use

Invoke this skill when:
- Debugging RAG integration issues
- Adding new oncological conditions to `CONDITIONS_REGISTRY`
- Modifying guardrails or validation rules
- Security audit and CVE mitigation verification
- PAE generation troubleshooting
- Understanding PicoClaw architecture

## Quick Reference

### Commands

```bash
# Launcher principal (recomendado)
./scripts/start-picoclaw.sh interactive   # REPL mode
./scripts/start-picoclaw.sh query "..."   # Single query
./scripts/start-picoclaw.sh pae           # Generate PAE
./scripts/start-picoclaw.sh status        # Health check

# Python module directo
python -m picoclaw extract <condition>    # Extract condition data
python -m picoclaw doctor                 # System diagnostics
```

### Key Files

| File | Purpose |
|------|---------|
| `scripts/picoclaw/cli.py` | Entry point (451 lines) |
| `scripts/picoclaw/core/domain.py` | Domain types (RAGResult, VerificationStatus) |
| `scripts/picoclaw/core/extraction_domain.py` | Clinical data structures |
| `scripts/picoclaw/core/guardrails.py` | NANDA/NOC/NIC validation |
| `scripts/picoclaw/core/prompts.py` | System prompts (SYSTEM, QUIZ, PAE) |
| `scripts/picoclaw/infrastructure/rag_bridge.py` | RAG integration wrapper |
| `scripts/picoclaw/infrastructure/deepseek_client.py` | LLM client via OpenAI SDK |
| `scripts/picoclaw/infrastructure/extraction_client.py` | LLM + RAG orchestrator |
| `scripts/picoclaw/infrastructure/yaml_repository.py` | Persistence layer |

## Architecture

```
scripts/picoclaw/
├── cli.py                   # Entry point CLI
├── core/
│   ├── domain.py            # RAGResult, AgentResponse, VerificationStatus
│   ├── extraction_domain.py # EpidemiologiaChile, FactorRiesgo, DiagnosticoNANDA...
│   ├── guardrails.py        # Clinical validation (NANDA/NOC/NIC patterns)
│   └── prompts.py           # SYSTEM_PROMPT, QUIZ_SYSTEM_PROMPT, PAE_SYSTEM_PROMPT
└── infrastructure/
    ├── deepseek_client.py   # LLM client via OpenAI SDK
    ├── extraction_client.py # Orchestrator LLM + RAG
    ├── rag_bridge.py        # Wrapper for scripts/rag.sh
    └── yaml_repository.py   # Persistence in vault/00-metadatos/datos-afecciones.md
```

### Data Flow

```
User Query
    │
    ▼
┌─────────────┐
│  CLI        │─── interactive / query / extract / doctor
└─────┬───────┘
      │
      ▼
┌──────────────────┐     ┌────────────────┐
│  RAGBridge       │────▶│ scripts/rag.sh │
└──────┬───────────┘     └────────────────┘
       │
       ▼
┌──────────────────┐     ┌────────────────┐
│  DeepSeekClient  │────▶│ DeepSeek API   │
└──────┬───────────┘     └────────────────┘
       │
       ▼
┌──────────────────┐
│  Guardrails      │ (NANDA/NOC/NIC validation)
└──────┬───────────┘
       │
       ▼
   AgentResponse
```

## Verification Status

| Status | Meaning | When to use |
|--------|---------|-------------|
| `VERIFICADO` | RAG similarity >= 0.60 | RAG confirms the data |
| `ASUMIDO` | From config without verification | RAG unavailable or no match |
| `COMPLETAR` | Missing data | Requires research |

## Security Model

### CVE Mitigations

| CVE | Issue | Mitigation |
|-----|-------|------------|
| CVE-2026-25253 | Token exfiltration via Web UI | CLI-only (no Web UI) |
| CVE-2026-24763 | Command injection via PATH | Shell allowlist only |

### Security Gates

| Gate | Check |
|------|-------|
| Workspace Restriction | `restrict_to_workspace: true` |
| Hardcoded API Keys | No `sk-*` in config |
| Shell Mode | `allowlist` only |
| Web Access | `enabled: false` |
| Gateway Binding | `127.0.0.1` only |

### Security Scripts

```bash
# Run security audit
./scripts/picoclaw_security_check.sh

# Sanitize environment
./scripts/picoclaw_env_sanitizer.sh
```

## CONDITIONS_REGISTRY

PicoClaw manages **14 oncological conditions** for EEO-2025:

**Módulo A - Tumores Sólidos:**
1. `cancer-mama` - Cáncer de mama (GES)
2. `cancer-pulmon` - Cáncer de pulmón (GES)
3. `cancer-colon` - Cáncer de colon (GES)
4. `cancer-gastrico` - Adenocarcinoma gástrico (GES)
5. `cancer-recto` - Adenocarcinoma de recto (GES)
6. `cancer-cervicouterino` - Cáncer cervicouterino (GES)
7. `cancer-testicular` - Cáncer testicular (GES)
8. `cancer-tiroides` - Cáncer de tiroides
9. `cancer-esofago` - Cáncer de esófago
10. `carcinoma-anal` - Carcinoma de canal anal

**Módulo B - Neoplasias Hematológicas:**
11. `leucemia-linfoblastica` - Leucemia linfoblástica aguda (GES)
12. `leucemia-mieloide` - Leucemia mieloide aguda (GES)
13. `linfoma-hodgkin` - Linfoma no Hodgkin (GES)
14. `mieloma-multiple` - Mieloma múltiple (GES)

## Troubleshooting

### RAG Not Responding

1. Check `scripts/rag.sh` status
2. Verify Ollama is running: `ollama ps`
3. Check INDEX_OK file exists
4. Run `./scripts/start-picoclaw.sh status`

### Security Check Fails

1. Run `./scripts/picoclaw_security_check.sh`
2. Check each gate output
3. Fix config at `~/.picoclaw/config.json`
4. Re-run sanitizer: `./scripts/picoclaw_env_sanitizer.sh`

### Extraction Fails

1. Check DeepSeek API key in `.env`
2. Verify condition ID in `CONDITIONS_REGISTRY`
3. Check RAG availability
4. Check logs for error details

### PAE Generation Issues

1. Verify condition exists in `datos-afecciones.md`
2. Check YAML structure is valid
3. Ensure RAG is available for verification
4. Run `python -m picoclaw doctor` for diagnostics

## Adding New Conditions

To add a new oncological condition:

1. **Add to CONDITIONS_REGISTRY** in `cli.py`:
   ```python
   CONDITIONS_REGISTRY = {
       # ... existing conditions ...
       "nueva-afeccion": "Nueva Afección Oncológica",
   }
   ```

2. **Add YAML data** in `vault/00-metadatos/datos-afecciones.md`:
   ```yaml
   nueva-afeccion:
     nombre: "Nueva Afección Oncológica"
     ges: true/false
     # ... full structure ...
   ```

3. **Add clinical documents** to corpus:
   - Place in `scripts/corpus/` for RAG indexing
   - Re-run indexing if needed

4. **Test extraction**:
   ```bash
   python -m picoclaw extract nueva-afeccion
   ```

## Modifying Guardrails

Guardrails validate clinical content against NANDA/NOC/NIC patterns.

Location: `scripts/picoclaw/core/guardrails.py`

Key patterns:
- `NANDA_PATTERN` - Validates NANDA diagnosis format
- `NOC_PATTERN` - Validates NOC outcome format
- `NIC_PATTERN` - Validates NIC intervention format
- `VERIFICATION_PATTERN` - Validates verification status

## Integration with Other Skills

- **pae-generator**: Uses PicoClaw for RAG verification
- **citation-check**: Verifies clinical citations
- **flashcards**: Can use PicoClaw for content generation
- **quiz**: Uses PicoClaw quiz mode

## Configuration

### Config File: `~/.picoclaw/config.json`

```json
{
  "restrict_to_workspace": true,
  "shell_mode": "allowlist",
  "allowed_commands": ["rag.sh", "python", "node"],
  "web_access": false,
  "gateway_host": "127.0.0.1",
  "gateway_port": 8080
}
```

### Environment Variables

```bash
DEEPSEEK_API_KEY=sk-...    # Required for LLM
PICOCLAW_WORKSPACE=/path   # Optional workspace override
```

## Maintenance Tasks

### Health Check

```bash
./scripts/start-picoclaw.sh status
```

Expected output:
```
✓ RAG Bridge: OK
✓ DeepSeek Client: OK
✓ YAML Repository: OK
✓ Guardrails: OK
All systems operational
```

### Diagnostics

```bash
python -m picoclaw doctor
```

---

_Skill v1.0 — PicoClaw Expert Knowledge Base_
_Compatible with PicoClaw v1.0+_
