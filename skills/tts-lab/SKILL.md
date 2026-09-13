---
name: tts-lab
description: "Use when doing text-to-speech, voice cloning from reference audio, Qwen3-TTS experiments, speaker-profile creation, or custom voice generation in the Tts_tq project."
when: "When the user asks for voice cloning, Qwen3-TTS, speech synthesis, reference-audio cloning, speaker profiles, custom voice generation, or work inside the Tts_tq repository."
examples:
  - "qwen3 tts voice cloning and speech synthesis"
  - "clone a voice from reference audio"
  - "generate a custom speaker profile"
  - "work in the Tts_tq project"
  - "create voice from reference wav"
  - "text to speech with qwen3"
license: MIT
metadata:
  author: Felipe Gonzalez
  version: "1.0.0"
  openclaw:
    requires:
      bins: ["uv", "python3"]
      anyBins: ["uv", "pip"]
    emoji: "🎙️"
    primaryEnv: null
---

# TTS Lab - Voice Cloning Laboratory Guide

Guía completa para trabajar con el laboratorio de TTS en `~/Developer/Tts_tq`.

## Quick Start

```bash
# Ir al proyecto
cd ~/Developer/Tts_tq

# Instalar dependencias
uv sync --dev

# Generar voz con speaker predefinido
uv run tts-generate speech "Hola mundo" -l Spanish -s Serena -o output/test.wav

# Clonar voz desde referencia
uv run tts-clone voice \
    voice_profiles/felipe/reference.wav \
    -r "Texto de la referencia" \
    -t "Texto a sintetizar" \
    -o output/cloned.wav
```

## Project Structure

```
Tts_tq/
├── src/tts_lab/          # Source code (Clean Architecture)
│   ├── domain/           # PURE - Entities, Protocols, Exceptions
│   ├── application/      # Orchestration - Use Cases, DTOs
│   └── infrastructure/   # IMPURE - QwenClient, FileStorage, Config
│
├── voice_profiles/       # Saved voice profiles
│   └── felipe/           # Felipe's voice profile
│       ├── reference.wav
│       ├── pitch_seg1.wav
│       └── metadata.json
│
├── output/               # Generated audio files
│   ├── felipe_cloned.wav
│   ├── ejemplo_1_icl_completo.wav
│   └── voice_matrix/
│
├── scripts/              # CLI entry points & utilities
│   ├── generate_voice_matrix.py
│   ├── generate_voice_case.py
│   └── record_reference_v2.sh
│
├── tests/                # Test suite
│   ├── unit/             # Fast unit tests
│   └── integration/      # Slow integration tests
│
└── comfyui/              # ComfyUI integration (visual exploration)
```

## Architecture

**Pattern:** Clean Architecture con Pure Core / Impure Edge

```
┌─────────────────────────────────────────────────┐
│              TTS Lab Architecture                │
├─────────────────────────────────────────────────┤
│  CLI (Typer) → Application → Domain ← Infra     │
│                                                  │
│  Domain (Pure):                                  │
│    • Entities (TTSRequest, AudioResult)         │
│    • Protocols (TTSClient, AudioRepo)           │
│    • NO external dependencies                   │
│                                                  │
│  Infrastructure (Impure):                        │
│    • QwenTTSClient (model loading)              │
│    • FileAudioRepository (I/O)                  │
│    • Config (env vars)                          │
└─────────────────────────────────────────────────┘
```

## Key Components

### Domain Layer (Pure)

**Entities:**
- `TTSRequest`: text, language, speaker, instruct
- `AudioResult`: audio_data (bytes), sample_rate, duration
- `VoiceProfile`: name, reference_audio_path, reference_text

**Protocols:**
- `TTSClient`: generate(), clone_voice()
- `AudioRepository`: save(), save_with_hash(), load()

**Exceptions:**
- `TTSError`, `VoiceProfileError`, `ModelLoadError`, `AudioFormatError`

### Infrastructure Layer (Impure)

**QwenTTSClient:**
- Lazy loading (solo carga modelo cuando se necesita)
- Context manager para auto-cleanup
- Device auto-detect: MPS (Apple Silicon), CUDA, CPU

**FileAudioRepository:**
- Security: sanitización de filenames (path traversal protection)
- Content-based hashing para nombres únicos
- Path validation

### Application Layer

**GenerateSpeechUseCase:**
- Orquestación pura
- Delega side effects a infrastructure
- DTO pattern (Request/Response)

## Models

### 1. CustomVoice (Voces Predefinidas)

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="mps",
)

# 9 voces premium
speakers = ["Ryan", "Aiden", "Vivian", "Serena", "Uncle_Fu", 
            "Dylan", "Eric", "Ono_Anna", "Sohee"]

# 10 idiomas
languages = ["Spanish", "English", "Chinese", "Japanese", "Korean",
             "German", "French", "Russian", "Portuguese", "Italian"]

# Control emocional
wavs, sr = model.generate_custom_voice(
    text="Hola mundo",
    language="Spanish",
    speaker="Serena",
    instruct="Habla con tono amigable"  # Opcional
)
```

**Latencia:** ~97ms

### 2. Base Model (Voice Cloning)

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="mps",
)

# Zero-shot voice cloning desde 3 segundos
wavs, sr = model.generate_voice_clone(
    ref_audio=(audio_array, sample_rate),  # Tuple format!
    ref_text="Texto de la referencia",
    text="Nuevo texto a sintetizar",
    language="es",
)
```

**Latencia:** ~30-40s (sin flash-attn)

### 3. VoiceDesign (Crear Voces)

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="mps",
)

wavs, sr = model.generate_voice_design(
    text="Hola, esta es una voz diseñada.",
    language="Spanish",
    instruct="Voz femenina española de España, con acento castellano claro."
)
```

**Mejor para:** Español nativo sin acento extranjero

## CLI Commands

### Installation

```bash
cd ~/Developer/Tts_tq
uv sync --dev
```

### Generate Speech

```bash
# Con speaker predefinido
uv run tts-generate speech "Hola mundo" \
    -l Spanish \
    -s Serena \
    -o output/test.wav

# Con instrucciones de estilo
uv run tts-generate speech "Hola mundo" \
    -l Spanish \
    -s Ryan \
    -i "Habla rápido y emocionado" \
    -o output/fast.wav
```

### Clone Voice

```bash
# Desde referencia
uv run tts-clone voice \
    voice_profiles/felipe/reference.wav \
    -r "La tecnología de inteligencia artificial ha revolucionado..." \
    -t "Este es un nuevo texto con mi voz clonada" \
    -o output/cloned.wav

# Con modelo específico
uv run tts-clone voice \
    reference.wav \
    -r "Texto ref" \
    -t "Texto nuevo" \
    -m Qwen/Qwen3-TTS-12Hz-1.7B-Base \
    -d mps \
    -o output/cloned.wav
```

### Record Reference

```bash
# Grabar referencia interactiva (15 segundos)
./scripts/record_reference_v2.sh

# Requisitos:
# - 10-15 segundos
# - Sin ruido de fondo
# - Hablar claro y natural
# - Sin pausas largas
```

## Voice Profiles

### Structure

```
voice_profiles/
└── felipe/
    ├── README.md           # Instrucciones
    ├── metadata.json       # Metadatos
    ├── reference.wav       # Audio original (1.8 MB)
    ├── reference_clean.wav # Audio limpio (650 KB)
    ├── reference_v2.wav    # Segunda grabación (650 KB)
    ├── pitch_full.wav      # Full pitch range (12.6 MB)
    ├── pitch_seg1.wav      # Pitch segment 1
    ├── pitch_seg2.wav      # Pitch segment 2
    └── pitch_seg3.wav      # Pitch segment 3
```

### metadata.json

```json
{
    "name": "felipe",
    "description": "Voice profile for Felipe González",
    "language": "Spanish",
    "reference_audio": "reference.wav",
    "reference_text": "Record a 10-15 second sample...",
    "notes": [
        "Speak clearly with no background noise",
        "Use natural pace and intonation"
    ]
}
```

## Experimentation Scripts

### Voice Matrix

Genera matriz de comparación con diferentes configuraciones:

```bash
# Generar todos los casos
python scripts/generate_voice_matrix.py

# Generar caso específico
python scripts/generate_voice_case.py 01_refv2_auto_icl
```

**Casos disponibles:**
- `01_refv2_auto_icl` - Reference v2 con ICL (In-Context Learning)
- `02_refv2_spanish_icl` - Reference v2 con español explícito
- `03_refv2_auto_embedding` - Reference v2 solo embedding
- `04_pitch1_auto_icl` - Pitch segment 1 con ICL
- `05_pitch1_spanish_icl` - Pitch segment 1 con español
- `06_pitch1_auto_embedding` - Pitch segment 1 solo embedding
- `07_pitch2_auto_icl` - Pitch segment 2 con ICL
- `08_pitch3_auto_icl` - Pitch segment 3 con ICL

**Output:** `output/voice_matrix/` con 8 WAVs + manifest.json

## Testing

### Unit Tests (Fast)

```bash
# Run unit tests
uv run pytest tests/unit/ -v

# With coverage
uv run pytest tests/unit/ --cov=src --cov-report=html

# Parallel execution
uv run pytest -n auto
```

### Integration Tests (Slow)

```bash
# Requires model download
uv run pytest tests/integration/ -v -m slow
```

### Test Structure

```
tests/
├── unit/
│   ├── test_entities.py      # Domain entities
│   ├── test_protocols.py     # Domain protocols
│   ├── test_use_cases.py     # Application layer
│   ├── test_qwen_client.py   # Infrastructure client
│   └── test_file_storage.py  # Infrastructure storage
│
└── integration/
    └── test_voice_cloning.py # End-to-end tests
```

## Configuration

### Environment Variables

```bash
# .env (optional)
TTS_MODEL_PATH=Qwen/Qwen3-TTS-12Hz-1.7B-Base
TTS_DEVICE=mps              # mps, cuda, cpu
TTS_OUTPUT_DIR=output
TTS_VOICES_DIR=voice_profiles
```

### Config Class

```python
from tts_lab.infrastructure.config import TTSConfig

# From environment
config = TTSConfig.from_env()

# Manual
config = TTSConfig(
    model_path="Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device="mps",
    output_dir="output",
    voices_dir="voice_profiles"
)
```

## Python API

### Generate Speech

```python
from tts_lab.infrastructure.qwen_client import QwenTTSClient
from tts_lab.infrastructure.file_storage import FileAudioRepository
from tts_lab.application.use_cases import GenerateSpeechUseCase
from tts_lab.application.dto import GenerateSpeechRequest

# Context manager para auto-cleanup
with QwenTTSClient(
    model_path="Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device="mps"
) as client:
    repo = FileAudioRepository(output_dir="output")
    use_case = GenerateSpeechUseCase(tts_client=client, audio_repo=repo)

    request = GenerateSpeechRequest(
        text="Hola mundo",
        language="Spanish"
    )

    response = use_case.execute(request)
    print(f"Audio saved to: {response.audio_path}")
    print(f"Duration: {response.duration_seconds:.2f}s")
```

### Clone Voice

```python
from tts_lab.domain.entities import VoiceProfile

profile = VoiceProfile(
    name="felipe",
    reference_audio_path="voice_profiles/felipe/reference.wav",
    reference_text="La tecnología de inteligencia artificial..."
)

with QwenTTSClient(model_path="...", device="mps") as client:
    audio = client.clone_voice(profile, "Este texto será hablado con mi voz!")
    
    repo = FileAudioRepository(output_dir="output")
    path = repo.save(audio, "cloned.wav")
    print(f"Cloned audio: {path}")
```

## Output Examples

### Generated Files

```
output/
├── ejemplo_1_icl_completo.wav       # 914 KB - Full ICL
├── ejemplo_2_embedding_neutral.wav  # 530 KB - Solo embedding
├── ejemplo_3_temp_baja.wav          # 1.4 MB - Temperatura baja
├── ejemplo_4_temp_alta.wav          # 1.2 MB - Temperatura alta
├── ejemplo_5_serena.wav             # 177 KB - Serena voice
├── ejemplo_5_aiden.wav              # 150 KB - Aiden voice
├── ejemplo_5_vivian.wav             # 242 KB - Vivian voice
├── ejemplo_6_voz_disenada.wav       # 119 KB - VoiceDesign
│
├── felipe_cloned.wav                # 818 KB - Tu voz clonada
├── felipe_embedding_only.wav        # 457 KB - Solo embedding
├── felipe_icl.wav                   # 361 KB - ICL
├── felipe_neutral.wav               # 1.4 MB - Versión neutral
│
└── voice_matrix/                    # Matriz de comparación
    ├── 01_refv2_auto_icl.wav
    ├── 02_refv2_spanish_icl.wav
    ├── 03_refv2_auto_embedding.wav
    └── manifest.json
```

## Design Lessons

### 1. Pure Core / Impure Edge

**Domain layer es 100% puro:**
- No imports de torch, transformers, etc.
- Solo dataclasses y Protocols
- Fácil de testear con mocks

**Infrastructure layer maneja side effects:**
- Model loading
- File I/O
- Network calls

### 2. Lazy Loading

```python
def _ensure_model_loaded(self):
    if self._model is None:
        self._model = load_heavy_model()
```

**Beneficio:** Solo carga el modelo cuando se necesita, ahorra memoria.

### 3. Context Manager

```python
with QwenTTSClient(...) as client:
    audio = client.generate(request)
# Auto-cleanup al salir
```

**Beneficio:** Liberación automática de recursos.

### 4. Content-Based Hashing

```python
hash_input = f"{text}_{language}".encode()
content_hash = hashlib.sha256(hash_input).hexdigest()[:12]
filename = f"speech_{content_hash}.wav"
```

**Beneficio:** Nombres únicos, cache-friendly, reproducible.

### 5. Security-First

```python
def _sanitize_filename(self, filename: str) -> str:
    safe = Path(filename).name  # Remove path separators
    if not safe.endswith(".wav"):
        safe = f"{safe}.wav"
    return safe
```

**Beneficio:** Previene path traversal attacks.

## Common Workflows

### Workflow 1: Generar Voz con Speaker

```bash
# 1. Ir al proyecto
cd ~/Developer/Tts_tq

# 2. Generar voz
uv run tts-generate speech "Hola Felipe, ¿cómo estás?" \
    -l Spanish \
    -s Serena \
    -o output/greeting.wav

# 3. Escuchar
afplay output/greeting.wav
```

### Workflow 2: Clonar Voz

```bash
# 1. Grabar referencia (si no existe)
./scripts/record_reference_v2.sh

# 2. Clonar voz
uv run tts-clone voice \
    voice_profiles/felipe/reference_v2.wav \
    -r "La tecnología de inteligencia artificial ha revolucionado la forma en que interactuamos con los dispositivos. Cada día descubrimos nuevas aplicaciones que facilitan nuestras tareas diarias." \
    -t "Hola, esta es mi voz clonada hablando español." \
    -o output/my_cloned_voice.wav

# 3. Escuchar resultado
afplay output/my_cloned_voice.wav
```

### Workflow 3: Experimentar con Configuraciones

```bash
# 1. Generar matriz de comparación
python scripts/generate_voice_matrix.py

# 2. Revisar resultados
ls -lh output/voice_matrix/

# 3. Escuchar diferentes configuraciones
afplay output/voice_matrix/01_refv2_auto_icl.wav
afplay output/voice_matrix/03_refv2_auto_embedding.wav
```

### Workflow 4: Crear Voz Diseñada

```python
# voice_design_test.py
from qwen_tts import Qwen3TTSModel
import soundfile as sf

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="mps",
)

wavs, sr = model.generate_voice_design(
    text="Hola, esta es una voz chilena natural.",
    language="Spanish",
    instruct="Voz femenina chilena de Santiago, con acento suave y tono cálido."
)

sf.write("output/chilean_voice.wav", wavs[0], sr)
```

## Troubleshooting

### Model Loading Errors

```bash
# Verificar que el modelo existe
ls -la comfyui/models/qwen-tts/

# Verificar memoria disponible
vm_stat | head -10

# Usar CPU si MPS falla
export TTS_DEVICE=cpu
```

### Audio Quality Issues

```bash
# Verificar formato de referencia
sox --info voice_profiles/felipe/reference.wav

# Limpiar audio de referencia
sox reference.wav reference_clean.wav \
    highpass 100 \
    lowpass 8000 \
    norm -3
```

### Performance Optimization

```bash
# Instalar flash-attn para reducir latencia (30s → 10s)
pip install flash-attn --no-build-isolation

# Verificar device
python -c "import torch; print(torch.backends.mps.is_available())"
```

## Mejorar Calidad de Clonación

**Ver guía completa:** `resources/voice-cloning-improvement-guide.md`

### Factores Clave (3)

1. **Audio de referencia:** 10-15 segundos, limpio, sin ruido
2. **Transcripción precisa:** Mejora similitud de 0.75 → 0.89
3. **Modo correcto:** ICL (calidad) vs Embedding (velocidad)

### Modos de Clonación

**ICL Mode (Full):**
```python
model.generate_voice_clone(
    text="Nuevo texto",
    ref_audio="reference.wav",
    ref_text="Transcripción exacta",  # CRÍTICO
    x_vector_only_mode=False  # Full ICL
)
```
- ✅ Mayor calidad (0.89 similitud)
- ✅ Captura prosodia
- ⚠️ Requiere transcripción

**Embedding Mode:**
```python
model.generate_voice_clone(
    text="Nuevo texto",
    ref_audio="reference.wav",
    ref_text="",  # No necesario
    x_vector_only_mode=True  # Embedding
)
```
- ✅ Sin transcripción
- ✅ Más rápido
- ⚠️ Menor calidad (0.75 similitud)

### Optimizaciones de Rendimiento

**FlashAttention 2:**
```bash
pip install -U flash-attn --no-build-isolation
```
- Reduce VRAM 30-40%
- Mejora velocidad <5%

**CUDA Graphs (faster-qwen3-tts):**
```bash
pip install faster-qwen3-tts
```
- Speedup 5-10x en GPUs NVIDIA
- TTFA: 156ms en RTX 4090
- RTF: 4.78 (4.78x más rápido que tiempo real)

### Workflow VoiceDesign → Clone

```python
# 1. Diseñar voz ideal
wavs, sr = model.generate_voice_design(
    text="Hola",
    language="Spanish",
    instruct="Voz masculina chilena, 30 años, tono cálido"
)
sf.write("designed.wav", wavs[0], sr)

# 2. Transcribir con Whisper
import whisper
whisper_model = whisper.load_model("base")
result = whisper_model.transcribe("designed.wav")

# 3. Usar como referencia
model_base.generate_voice_clone(
    text="Nuevo texto",
    ref_audio="designed.wav",
    ref_text=result["text"]
)
```

### Troubleshooting Común

**Artefacto en primera palabra:**
- Agregar 0.5s silencio al final del reference

**Acento incorrecto cross-lingual:**
- Usar modo embedding-only

**Generación se cuelga:**
- Recortar reference a 10-15s

**Calidad baja:**
- Usar modelo 1.7B (no 0.6B)
- Verificar transcripción con Whisper

---

## Next Steps

1. **Integrar con OpenClaw**: Crear servidor HTTP que use este sistema
2. **Optimizar latencia**: Instalar flash-attn para reducir 30s → 10s
3. **Explorar VoiceDesign**: Crear voz personalizada desde descripción
4. **Batch processing**: Generar múltiples audios en paralelo
5. **API REST**: Exponer como servicio con FastAPI

## Resources

- **README:** `~/Developer/Tts_tq/README.md`
- **Tests:** `~/Developer/Tts_tq/tests/`
- **Output:** `~/Developer/Tts_tq/output/`
- **Voice Profiles:** `~/Developer/Tts_tq/voice_profiles/`
- **ComfyUI:** `~/Developer/Tts_tq/comfyui/`
- **MEJORA CLONACIÓN:** `resources/voice-cloning-improvement-guide.md` ⭐

---

**Version:** 1.1.0
**Created:** 2026-03-12
**Updated:** 2026-03-12 (added voice cloning improvement guide)
**Author:** PicoClaw
**Status:** Active
**Project:** ~/Developer/Tts_tq
