# Guía Completa: Mejorar Clonado de Voz con Qwen3-TTS

**Basado en investigación actualizada - Marzo 2026**

---

## 🎯 Resumen Ejecutivo

**Los 3 factores más importantes para calidad de clonación:**
1. **Audio de referencia correcto** (10-15 segundos, limpio)
2. **Transcripción precisa** (mejora similitud de 0.75 → 0.89)
3. **Modo de clonación adecuado** (ICL vs Embedding según caso)

---

## 📊 Comparación de Modos de Clonación

### ICL Mode (In-Context Learning) - Full Mode

**Activación:** `x_vector_only_mode=False` (default)

**Características:**
- ✅ **Mayor calidad:** Usa speaker embedding + audio codec tokens
- ✅ **Mejor similitud:** 0.89 vs 0.75 sin transcripción
- ✅ **Captura prosodia:** Ritmo, entonación, patrones de habla
- ⚠️ **Requiere transcripción:** Texto exacto del audio de referencia
- ⚠️ **Más lento:** 80+ tokens de prefill
- ⚠️ **Artefacto inicial:** Puede "bleedear" el último fonema de referencia

**Casos de uso:**
- Calidad máxima requerida
- Tienes transcripción exacta
- Producción de audiolibros
- Contenido profesional

**Ejemplo:**
```python
wavs, sr = model.generate_voice_clone(
    text="Nuevo texto a sintetizar",
    language="Spanish",
    ref_audio="reference.wav",
    ref_text="Transcripción exacta del audio de referencia",  # CRÍTICO
    x_vector_only_mode=False  # Full ICL mode
)
```

---

### Embedding-Only Mode (X-Vector)

**Activación:** `x_vector_only_mode=True`

**Características:**
- ✅ **Sin transcripción:** No requiere ref_text
- ✅ **Más rápido:** Solo 10 tokens de prefill
- ✅ **Sin artefactos:** No hay bleed del audio de referencia
- ✅ **Reutilizable:** Embedding de 4KB (2048-dim bf16 vector)
- ✅ **Cross-lingual mejor:** Sin "accent bleed" del idioma original
- ⚠️ **Menor calidad:** Solo captura timbre, no prosodia
- ⚠️ **Similitud reducida:** ~0.75 vs 0.89 de ICL

**Casos de uso:**
- No tienes transcripción
- Velocidad prioritaria
- Múltiples idiomas
- Prototipado rápido

**Ejemplo:**
```python
wavs, sr = model.generate_voice_clone(
    text="Nuevo texto a sintetizar",
    language="Spanish",
    ref_audio="reference.wav",
    ref_text="",  # No necesario
    x_vector_only_mode=True  # Embedding only
)
```

---

## 🎙️ Especificaciones de Audio de Referencia

### Duración Óptima: 10-15 Segundos

**¿Por qué 15 segundos?**

El tokenizer de Qwen3-TTS opera a 12.5 Hz con 16 capas de codebook:
- 15 segundos = ~188 codec tokens
- Suficiente para capturar: timbre, pitch contour, speaking style
- No abruma el context window del modelo

**Problemas con audio más largo:**
- 60 segundos = ~750 tokens de prefill
- Aumenta coste computacional drásticamente
- Riesgo de "generation hangs" (modelo no emite EOS token)
- **No mejora calidad** - el modelo se confunde

**Problemas con audio más corto:**
- 3 segundos = mínimo viable (feature oficial)
- Calidad escala linealmente de 3 → 15 segundos
- Menos de 3 segundos: insuficiente para capturar características

### Especificaciones Técnicas

| Parámetro | Requerido | Óptimo |
|-----------|-----------|--------|
| **Formato** | WAV 16-bit, MP3, M4A | WAV 16-bit |
| **Sample rate** | ≥24 kHz | 24 kHz |
| **Canales** | Mono | Mono |
| **Tamaño** | <10 MB | <5 MB |
| **Discurso continuo** | ≥3 segundos | 10-15 segundos |
| **Ocupación de voz** | ≥60% del audio | 100% |
| **Pausas máximas** | ≤2 segundos | Sin pausas |

### Calidad de Audio

**REQUERIDO:**
- ✅ Sin ruido de fondo
- ✅ Sin música
- ✅ Sin eco/reverberación excesiva
- ✅ Volumen consistente
- ✅ Sin cortes/glitches

**PROHIBIDO:**
- ❌ Cantar (a menos que quieras clonar voz de canto)
- ❌ Susurrar (a menos que quieras voz susurrada)
- ❌ Efectos de sonido
- ❌ Múltiples hablantes
- ❌ Ruido ambiental (TV, tráfico, etc.)

**RECOMENDADO:**
- 🎯 Grabación en ambiente silencioso
- 🎯 Micrófono de calidad (o iPhone)
- 🎯 Distancia consistente al micrófono
- 🎯 Hablar con ritmo natural
- 🎯 Incluir variación de entonación

### Contenido del Audio

**El modelo captura PROSODIA, no solo semántica:**

**✅ BUENO:**
- Discurso conversacional normal
- Entonación expresiva (ejemplo oficial incluye: "I love you. I respect you. But you know what? You blew it!")
- Variación de pitch natural
- Ritmo de habla típico

**❌ MALO:**
- Lectura monótona → clon monótono
- Tono inconsistente → modelo confundido
- Estilos muy diferentes en 15 segundos → disonancia

**Tip:** El audio de referencia enseña al modelo CÓMO hablas, no solo cómo SUENAS.

---

## 🔧 Transcripción Precisa: El Factor Clave

### Impacto en Calidad

**Sin transcripción (embedding-only):**
- Similitud de speaker: ~0.75
- Solo captura timbre básico

**Con transcripción exacta (ICL mode):**
- Similitud de speaker: ~0.89 (+18.7%)
- Captura timbre + prosodia + estilo

### Generación Automática de Transcripción

**Opción 1: Whisper (recomendado)**

```python
import whisper

# Cargar modelo
model = whisper.load_model("base")  # o "small", "medium", "large"

# Transcribir
result = model.transcribe("reference.wav")
transcription = result["text"]

print(f"Transcripción: {transcription}")
```

**Opción 2: OpenAI Whisper API**

```python
from openai import OpenAI

client = OpenAI()

with open("reference.wav", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print(transcription.text)
```

### Errores Comunes en Transcripción

**❌ ERRORES que degradan calidad:**
- Omisión de palabras
- Puntuación incorrecta
- Mayúsculas/minúsculas inconsistentes
- Palabras mal escritas
- Pausas no reflejadas

**✅ TRANSCRIPCIÓN IDEAL:**
```
"La tecnología de inteligencia artificial ha revolucionado 
la forma en que interactuamos con los dispositivos. Cada día 
descubrimos nuevas aplicaciones que facilitan nuestras 
tareas diarias."
```

**❌ TRANSCRIPCIÓN DEFECTUOSA:**
```
"la tecnologia de inteligencia artificial a revolucionado 
la forma en q interactuamos con los dispositivos cada dia 
descubrimos nuevas aplicaciones q facilitan nuestras tareas"
```

---

## 🚀 Optimizaciones de Rendimiento

### FlashAttention 2

**Beneficios:**
- Reduce uso de VRAM ~30-40%
- Mejora velocidad marginal (<5% según benchmarks)
- Permite batches más grandes

**Instalación:**

```bash
pip install -U flash-attn --no-build-isolation
```

**Requisitos:**
- CUDA GPU (no funciona en Mac MPS)
- PyTorch 2.1+
- Linux recomendado (Windows puede tener issues)

**Verificar instalación:**

```python
import torch
print(torch.cuda.is_available())  # True
print(hasattr(torch.nn.functional, 'scaled_dot_product_attention'))  # True
```

**Nota:** El proyecto faster-qwen3-tts reportó que FlashAttention dio <1% de mejora, por lo que lo eliminaron para simplificar. **No es crítico.**

---

### CUDA Graphs (Faster-Qwen3-TTS)

**Speedups reportados:**

| GPU | Baseline RTF | CUDA Graphs RTF | Speedup |
|-----|--------------|-----------------|---------|
| RTX 4090 | 0.82 | 4.78 | **5.8x** |
| RTX 4060 | 0.23 | 2.26 | **9.8x** |
| H100 | 0.435 | 3.884 | **8.9x** |

**RTF > 1.0 = más rápido que tiempo real**

**Instalación:**

```bash
pip install faster-qwen3-tts
```

**Uso:**

```python
from faster_qwen3_tts import FasterQwen3TTS

model = FasterQwen3TTS.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base")

# Streaming con chunks
for audio_chunk, sr, timing in model.generate_voice_clone_streaming(
    text="Hola mundo",
    language="Spanish",
    ref_audio="reference.wav",
    ref_text="Transcripción exacta",
    chunk_size=8,  # 8 steps ≈ 667ms de audio por chunk
):
    # Procesar cada chunk inmediatamente
    play(audio_chunk, sr)
```

**Requisitos:**
- PyTorch 2.5.1+ (2.5.0 tiene bugs en CUDA graph capture)
- NVIDIA GPU con CUDA
- No funciona en Mac

---

### Streaming vs Non-Streaming

**Streaming (recomendado para tiempo real):**

| Chunk Size | TTFA (ms) | RTF | Audio por chunk |
|------------|-----------|-----|-----------------|
| 1 | 240 | 0.750 | 83ms |
| 2 | 266 | 1.042 | 167ms |
| 4 | 362 | 1.251 | 333ms |
| 8 | 556 | 1.384 | 667ms |
| 12 | 753 | 1.449 | 1000ms |

**TTFA = Time To First Audio** (latencia inicial)

**Non-Streaming:**
- RTF: 1.57
- Espera todo el audio antes de retornar

**Recomendación:**
- chunk_size=8 para balance latencia/overhead
- chunk_size=2 para latencia mínima (real-time estricto)

---

## 🎨 Voice Design → Clone Workflow

**Problema:** VoiceDesign crea voces pero no son reutilizables.

**Solución:** VoiceDesign → Clone Pipeline

**Paso 1: Diseñar voz ideal**

```python
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="mps",
)

wavs, sr = model.generate_voice_design(
    text="Hola, esta es una voz de prueba.",
    language="Spanish",
    instruct=(
        "Voz masculina chilena de 30 años. "
        "Tono medio, ritmo conversacional, "
        "ligero acento santiaguino, "
        "voz cálida y amigable."
    )
)

# Guardar como referencia
import soundfile as sf
sf.write("designed_voice.wav", wavs[0], sr)
```

**Paso 2: Transcribir automáticamente**

```python
import whisper

whisper_model = whisper.load_model("base")
result = whisper_model.transcribe("designed_voice.wav")
transcription = result["text"]
```

**Paso 3: Usar como referencia para cloning**

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="mps",
)

wavs, sr = model.generate_voice_clone(
    text="Cualquier texto nuevo con la voz diseñada",
    language="Spanish",
    ref_audio="designed_voice.wav",
    ref_text=transcription,  # Transcripción del paso 2
)

sf.write("output.wav", wavs[0], sr)
```

**Ventajas:**
- ✅ Voz diseñada a medida
- ✅ Reutilizable indefinidamente
- ✅ Control total de características
- ✅ Sin necesidad de grabar

---

## 🧹 Preprocesamiento de Audio

### Reducción de Ruido

**Opción 1: Noisereduce (Python)**

```python
import noisereduce as nr
import soundfile as sf

# Cargar audio
audio, sr = sf.read("reference_noisy.wav")

# Reducir ruido
reduced_noise = nr.reduce_noise(y=audio, sr=sr)

# Guardar
sf.write("reference_clean.wav", reduced_noise, sr)
```

**Instalación:**

```bash
pip install noisereduce
```

---

**Opción 2: UVR5 (GUI - Recomendado para audio muy ruidoso)**

**Características:**
- Separa voz de música/ruido
- Calidad profesional
- Interface gráfica
- Modelos pre-entrenados

**Uso:**
1. Descargar UVR5
2. Cargar audio con ruido
3. Seleccionar modelo "MDX-Net"
4. Exportar solo voz

**Link:** https://github.com/Anjok07/ultimatevocalremovergui

---

### Normalización

```python
import soundfile as sf
import numpy as np

# Cargar
audio, sr = sf.read("reference.wav")

# Normalizar a -3 dB
max_val = max(abs(audio))
normalized = audio / max_val * 0.95  # 95% del máximo

# Guardar
sf.write("reference_normalized.wav", normalized, sr)
```

---

### Filtros de Frecuencia

```python
import soundfile as sf
import scipy.signal as signal

# Cargar
audio, sr = sf.read("reference.wav")

# Filtro pasa-altos (eliminar ruido grave)
b, a = signal.butter(5, 100/(sr/2), btype='high')
filtered = signal.filtfilt(b, a, audio)

# Filtro pasa-bajos (eliminar ruido agudo)
b, a = signal.butter(5, 8000/(sr/2), btype='low')
filtered = signal.filtfilt(b, a, filtered)

# Guardar
sf.write("reference_filtered.wav", filtered, sr)
```

---

## 🐛 Troubleshooting Común

### Problema 1: Artefacto en la Primera Palabra

**Síntoma:** El audio generado tiene un "glitch" o sonido extraño en la primera palabra.

**Causa:** En modo ICL, el modelo "continúa" el audio de referencia, causando bleed del último fonema.

**Solución:** Agregar 0.5 segundos de silencio al final del audio de referencia.

```python
import soundfile as sf
import numpy as np

# Cargar
audio, sr = sf.read("reference.wav")

# Agregar 0.5s de silencio
silence = np.zeros(int(sr * 0.5))
audio_with_silence = np.concatenate([audio, silence])

# Guardar
sf.write("reference_fixed.wav", audio_with_silence, sr)
```

---

### Problema 2: Acento Incorrecto en Cross-Lingual

**Síntoma:** Al clonar voz en español y generar en inglés, suena con acento español.

**Causa:** Modo ICL captura patrones del idioma original.

**Solución:** Usar modo embedding-only para cross-lingual.

```python
wavs, sr = model.generate_voice_clone(
    text="Hello world",
    language="English",
    ref_audio="spanish_reference.wav",
    ref_text="",  # Vacío
    x_vector_only_mode=True  # Embedding only
)
```

---

### Problema 3: Generación Se Cuelga (Hangs)

**Síntoma:** El modelo nunca termina de generar audio.

**Causa:** Audio de referencia muy largo (>30 segundos).

**Solución:** Recortar a 10-15 segundos.

```python
import soundfile as sf

# Cargar
audio, sr = sf.read("reference_long.wav")

# Recortar a 15 segundos
audio_trimmed = audio[:int(sr * 15)]

# Guardar
sf.write("reference_trimmed.wav", audio_trimmed, sr)
```

---

### Problema 4: Calidad Baja en 0.6B Model

**Síntoma:** Audio generado tiene calidad inferior, especialmente en idiomas no chinos.

**Causa:** Modelo 0.6B tiene menos capacidad.

**Solución:** Usar modelo 1.7B para mejor calidad.

```python
# ❌ Evitar para producción
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-0.6B-Base"
)

# ✅ Recomendado
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
)
```

**VRAM requerida:**
- 0.6B: 4-6 GB
- 1.7B: 6-8 GB

---

### Problema 5: Out of Memory

**Síntoma:** Error CUDA out of memory.

**Soluciones:**

**1. Reducir batch size:**
```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-0.6B-Base",  # Usar 0.6B
    device_map="cuda:0",
    torch_dtype=torch.float16  # FP16
)
```

**2. Usar CPU:**
```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
    device_map="cpu"
)
```

**3. Instalar FlashAttention:**
```bash
pip install flash-attn --no-build-isolation
```

---

## 📈 Benchmarks de Referencia

### Quality Metrics

| Modelo | Chinese WER | English WER | Speaker Similarity |
|--------|-------------|-------------|-------------------|
| Qwen3-TTS-1.7B | 2.12% | 2.58% | **0.89** |
| MiniMax | 2.45% | 2.83% | 0.85 |
| SeedTTS | 2.67% | 2.91% | 0.83 |
| ElevenLabs | 2.89% | 3.15% | 0.81 |

### Performance Metrics

| GPU | Modelo | RTF | TTFA | VRAM |
|-----|--------|-----|------|------|
| RTX 4090 | 1.7B | 0.82 | 800ms | 8 GB |
| RTX 4090 + CUDA Graphs | 1.7B | 4.78 | 156ms | 8 GB |
| RTX 3090 | 1.7B | 1.26 | - | 8 GB |
| RTX 3090 | 0.6B | 0.86 | - | 6 GB |
| GTX 1080 | 0.6B | 2.11 | - | 6 GB |

**RTF > 1.0 = más rápido que tiempo real**

---

## 🛠️ Herramientas Recomendadas

### Grabación de Referencia

1. **Audacity** (gratis, cross-platform)
   - Grabación limpia
   - Reducción de ruido básica
   - Normalización

2. **iPhone Voice Memos** (calidad sorprendente)
   - Grabación en ambiente silencioso
   - Exportar como WAV

3. **REAPER** (profesional, $60)
   - Edición avanzada
   - Plugins de reducción de ruido

### Reducción de Ruido

1. **noisereduce** (Python, gratis)
   - Rápido, efectivo
   - Fácil de automatizar

2. **UVR5** (gratis)
   - Separación voz/música
   - Calidad profesional

3. **iZotope RX** (profesional, $129+)
   - Industry standard
   - Reparación avanzada

### Transcripción

1. **Whisper** (OpenAI, gratis/local)
   - Mejor accuracy
   - Multilingual
   - Modelo "base" suficiente

2. **Google Speech-to-Text** (API, $)
   - Rápido
   - Buen accuracy

3. **Transcripción manual** (mejor calidad)
   - 100% accuracy
   - Time-consuming

---

## ✅ Checklist de Calidad

Antes de generar audio clonado:

### Audio de Referencia
- [ ] Duración: 10-15 segundos
- [ ] Formato: WAV 16-bit, 24 kHz, mono
- [ ] Sin ruido de fondo
- [ ] Sin música/efectos
- [ ] Volumen consistente
- [ ] Entonación natural
- [ ] Sin pausas largas (>2s)
- [ ] Discurso continuo ≥3s

### Transcripción
- [ ] Generada con Whisper o similar
- [ ] Revisada manualmente
- [ ] Puntuación correcta
- [ ] Sin errores ortográficos
- [ ] Refleja pausas naturales

### Modelo
- [ ] 1.7B para máxima calidad
- [ ] 0.6B para velocidad
- [ ] FlashAttention instalado (opcional)
- [ ] CUDA disponible (si es GPU)

### Generación
- [ ] Modo ICL si tienes transcripción
- [ ] Modo Embedding si no tienes transcripción
- [ ] 0.5s silencio al final (si hay artefacto inicial)
- [ ] Idioma consistente con referencia (para mejor calidad)

---

## 📚 Referencias

1. **Qwen3-TTS Official GitHub:** https://github.com/QwenLM/Qwen3-TTS
2. **Faster-Qwen3-TTS:** https://github.com/andimarafioti/faster-qwen3-tts
3. **Qwen3-TTS Voice Cloning Guide:** https://ocdevel.com/blog/20260302-qwen-tts-voice-cloning
4. **Complete 2026 Guide:** https://dev.to/czmilo/qwen3-tts-the-complete-2026-guide
5. **Alibaba Cloud API Docs:** https://www.alibabacloud.com/help/en/model-studio/qwen-tts-voice-cloning

---

**Versión:** 1.0.0
**Fecha:** 2026-03-12
**Autor:** PicoClaw 🦞
**Basado en:** Investigación web actualizada + documentación oficial + community feedback
