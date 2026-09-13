# CLI Reference - TTS Lab

## Installation

```bash
cd ~/Developer/Tts_tq
uv sync --dev
```

## Commands

### tts-generate

Generate speech with preset voices.

**Usage:**

```bash
uv run tts-generate speech TEXT [OPTIONS]
```

**Arguments:**

- `TEXT` - Text to convert to speech (required)

**Options:**

- `-o, --output PATH` - Output path (default: `output/speech.wav`)
- `-l, --language TEXT` - Language: Spanish, English, Auto (default: Auto)
- `-s, --speaker TEXT` - Speaker name (default: Serena)
- `-i, --instruct TEXT` - Voice style instructions
- `-m, --model PATH` - Model ID or path (default: Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)
- `-d, --device TEXT` - Device: mps, cuda, cpu (default: mps)

**Examples:**

```bash
# Basic usage
uv run tts-generate speech "Hola mundo"

# With specific speaker
uv run tts-generate speech "Hello world" -l English -s Ryan

# With style instructions
uv run tts-generate speech "¡Hola!" -l Spanish -i "Habla emocionado"

# Custom output
uv run tts-generate speech "Test" -o output/test.wav

# Specific model
uv run tts-generate speech "Test" -m Qwen/Qwen3-TTS-12Hz-1.7B-Base
```

**Available Speakers:**

| Speaker | Language | Description |
|---------|----------|-------------|
| Ryan | English | Dynamic male, rhythmic drive |
| Aiden | English | Sunny American male, clear midrange |
| Vivian | Chinese | Female voice |
| Serena | Chinese | Female voice |
| Uncle_Fu | Chinese | Male voice |
| Dylan | Chinese | Male voice |
| Eric | Chinese | Male voice |
| Ono_Anna | Japanese | Female voice |
| Sohee | Korean | Female voice |

---

### tts-clone

Clone voice from reference audio.

**Usage:**

```bash
uv run tts-clone voice REFERENCE_AUDIO [OPTIONS]
```

**Arguments:**

- `REFERENCE_AUDIO` - Path to reference audio file (required)

**Options:**

- `-r, --ref-text TEXT` - Transcription of reference audio (required)
- `-t, --text TEXT` - Text to speak with cloned voice (required)
- `-o, --output PATH` - Output path (default: `output/cloned.wav`)
- `-m, --model PATH` - Model ID or path (default: Qwen/Qwen3-TTS-12Hz-1.7B-Base)
- `-d, --device TEXT` - Device: mps, cuda, cpu (default: mps)

**Examples:**

```bash
# Basic cloning
uv run tts-clone voice reference.wav \
    -r "Reference text transcription" \
    -t "New text to speak"

# With custom output
uv run tts-clone voice reference.wav \
    -r "Reference text" \
    -t "New text" \
    -o output/my_voice.wav

# With specific model
uv run tts-clone voice reference.wav \
    -r "Reference text" \
    -t "New text" \
    -m Qwen/Qwen3-TTS-12Hz-1.7B-Base \
    -d cuda
```

**Reference Requirements:**

- Duration: 10-15 seconds (minimum 3 seconds)
- Format: WAV, MP3, or FLAC
- Quality: No background noise, clear speech
- Content: Natural pace and intonation

---

## Helper Scripts

### record_reference_v2.sh

Interactive reference audio recorder.

**Usage:**

```bash
./scripts/record_reference_v2.sh
```

**Process:**

1. Displays instructions
2. Shows text to read
3. Waits for user confirmation
4. Records 15 seconds
5. Saves to `voice_profiles/felipe/reference_v2.wav`

**Requirements:**

- `sox` installed
- Microphone configured
- Quiet environment

---

### generate_voice_matrix.py

Generate comparison matrix with different configurations.

**Usage:**

```bash
python scripts/generate_voice_matrix.py
```

**Output:**

- `output/voice_matrix/*.wav` - 8 audio files
- `output/voice_matrix/manifest.json` - Metadata

**Cases:**

| Case | Reference | Language | Mode |
|------|-----------|----------|------|
| 01 | ref_v2 | auto | ICL |
| 02 | ref_v2 | spanish | ICL |
| 03 | ref_v2 | auto | embedding |
| 04 | pitch1 | auto | ICL |
| 05 | pitch1 | spanish | ICL |
| 06 | pitch1 | auto | embedding |
| 07 | pitch2 | auto | ICL |
| 08 | pitch3 | auto | ICL |

---

### generate_voice_case.py

Generate single case from voice matrix.

**Usage:**

```bash
python scripts/generate_voice_case.py CASE_NAME
```

**Examples:**

```bash
# Generate specific case
python scripts/generate_voice_case.py 01_refv2_auto_icl

# Generate embedding-only case
python scripts/generate_voice_case.py 03_refv2_auto_embedding
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TTS_MODEL_PATH` | `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | Model ID or path |
| `TTS_DEVICE` | `mps` | Device: mps, cuda, cpu |
| `TTS_OUTPUT_DIR` | `output` | Output directory |
| `TTS_VOICES_DIR` | `voice_profiles` | Voice profiles directory |

**Usage:**

```bash
# Set environment variables
export TTS_DEVICE=cuda
export TTS_OUTPUT_DIR=/tmp/tts_output

# Run command
uv run tts-generate speech "Test"
```

---

## Common Workflows

### Workflow 1: Quick Test

```bash
# Generate test audio
uv run tts-generate speech "Prueba de voz" -l Spanish -s Serena

# Listen
afplay output/speech.wav
```

### Workflow 2: Clone Your Voice

```bash
# 1. Record reference
./scripts/record_reference_v2.sh

# 2. Clone voice
uv run tts-clone voice voice_profiles/felipe/reference_v2.wav \
    -r "La tecnología de inteligencia artificial ha revolucionado..." \
    -t "Hola, esta es mi voz clonada."

# 3. Listen
afplay output/cloned.wav
```

### Workflow 3: Compare Configurations

```bash
# Generate matrix
python scripts/generate_voice_matrix.py

# Compare ICL vs embedding
afplay output/voice_matrix/01_refv2_auto_icl.wav
afplay output/voice_matrix/03_refv2_auto_embedding.wav
```

### Workflow 4: Batch Generation

```bash
# Generate multiple audios
for text in "Hola" "Adiós" "Gracias"; do
    uv run tts-generate speech "$text" -l Spanish -o "output/${text}.wav"
done
```

---

## Troubleshooting

### Model Not Found

```bash
# Check model path
ls -la comfyui/models/qwen-tts/

# Download model (if needed)
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base
```

### Device Errors

```bash
# Check MPS availability
python -c "import torch; print(torch.backends.mps.is_available())"

# Fallback to CPU
export TTS_DEVICE=cpu
```

### Memory Errors

```bash
# Check available memory
vm_stat | head -10

# Use CPU if GPU memory insufficient
export TTS_DEVICE=cpu
```

### Audio Quality Issues

```bash
# Check reference audio
sox --info voice_profiles/felipe/reference.wav

# Clean audio
sox reference.wav reference_clean.wav highpass 100 lowpass 8000 norm -3
```

---

## Make Commands

```bash
# Install dependencies
make install

# Install dev dependencies
make dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Run linting
make lint

# Format code
make format

# Type checking
make typecheck

# Security checks
make security

# Clean artifacts
make clean
```

---

**Version:** 1.0.0
**Last Updated:** 2026-03-12
