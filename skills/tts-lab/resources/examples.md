# TTS Lab Examples

## Example 1: Generate Speech with Custom Voice

```python
from tts_lab.infrastructure.qwen_client import QwenTTSClient
from tts_lab.infrastructure.file_storage import FileAudioRepository
from tts_lab.application.use_cases import GenerateSpeechUseCase
from tts_lab.application.dto import GenerateSpeechRequest

# Initialize with context manager
with QwenTTSClient(
    model_path="Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device="mps"
) as client:
    # Setup repository
    repo = FileAudioRepository(output_dir="output")
    
    # Create use case
    use_case = GenerateSpeechUseCase(tts_client=client, audio_repo=repo)
    
    # Create request
    request = GenerateSpeechRequest(
        text="Hola, esta es una prueba de voz con Serena.",
        language="Spanish"
    )
    
    # Execute
    response = use_case.execute(request)
    
    print(f"Audio saved to: {response.audio_path}")
    print(f"Duration: {response.duration_seconds:.2f}s")
```

---

## Example 2: Clone Voice from Reference

```python
from tts_lab.infrastructure.qwen_client import QwenTTSClient
from tts_lab.domain.entities import VoiceProfile

# Create voice profile
profile = VoiceProfile(
    name="felipe",
    reference_audio_path="voice_profiles/felipe/reference_v2.wav",
    reference_text=(
        "La tecnología de inteligencia artificial ha revolucionado "
        "la forma en que interactuamos con los dispositivos."
    )
)

# Clone voice
with QwenTTSClient(
    model_path="Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device="mps"
) as client:
    # Generate cloned audio
    audio = client.clone_voice(
        profile=profile,
        text="Hola, esta es mi voz clonada hablando español."
    )
    
    # Save to file
    with open("output/cloned.wav", "wb") as f:
        f.write(audio.audio_data)
    
    print(f"Duration: {audio.duration_seconds:.2f}s")
    print(f"Sample rate: {audio.sample_rate} Hz")
```

---

## Example 3: Voice Design (Create Custom Voice)

```python
from qwen_tts import Qwen3TTSModel
import soundfile as sf

# Load VoiceDesign model
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="mps",
)

# Generate designed voice
wavs, sr = model.generate_voice_design(
    text="Hola, esta es una voz diseñada desde cero.",
    language="Spanish",
    instruct=(
        "Voz femenina chilena de Santiago. "
        "Acento suave y natural. "
        "Tono cálido y amigable. "
        "Velocidad de habla normal."
    )
)

# Save audio
sf.write("output/designed_voice.wav", wavs[0], sr)
print("Voice designed and saved!")
```

---

## Example 4: Batch Generation

```python
from tts_lab.infrastructure.qwen_client import QwenTTSClient
from tts_lab.infrastructure.file_storage import FileAudioRepository

# List of texts to generate
texts = [
    "Hola, bienvenido.",
    "Por favor, espera un momento.",
    "Gracias por tu paciencia.",
    "El proceso ha sido completado.",
]

# Generate all in one session
with QwenTTSClient(device="mps") as client:
    repo = FileAudioRepository(output_dir="output/batch")
    
    for i, text in enumerate(texts):
        print(f"Generating {i+1}/{len(texts)}: {text}")
        
        # Generate
        from tts_lab.domain.entities import TTSRequest
        request = TTSRequest(text=text, language="Spanish")
        audio = client.generate(request)
        
        # Save
        filename = f"message_{i+1:02d}.wav"
        path = repo.save(audio, filename)
        print(f"  → {path}")

print("Batch generation complete!")
```

---

## Example 5: Compare ICL vs Embedding

```python
from qwen_tts import Qwen3TTSModel
import soundfile as sf

# Load Base model
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="mps",
)

# Reference audio
ref_audio = "voice_profiles/felipe/reference_v2.wav"
ref_text = "La tecnología de inteligencia artificial..."
target_text = "Hola, esta es una comparación de modos."

# Mode 1: ICL (In-Context Learning)
print("Generating with ICL mode...")
prompt_icl = model.create_voice_clone_prompt(
    ref_audio,
    ref_text,
    x_vector_only_mode=False  # Full ICL
)
wavs_icl, sr = model.generate_voice_clone(
    target_text,
    "auto",
    voice_clone_prompt=prompt_icl
)
sf.write("output/comparison_icl.wav", wavs_icl[0], sr)

# Mode 2: Embedding only
print("Generating with embedding mode...")
prompt_emb = model.create_voice_clone_prompt(
    ref_audio,
    ref_text,
    x_vector_only_mode=True  # Embedding only
)
wavs_emb, sr = model.generate_voice_clone(
    target_text,
    "auto",
    voice_clone_prompt=prompt_emb
)
sf.write("output/comparison_embedding.wav", wavs_emb[0], sr)

print("Comparison complete!")
print("- output/comparison_icl.wav (full ICL)")
print("- output/comparison_embedding.wav (embedding only)")
```

---

## Example 6: Generate with Emotional Control

```python
from tts_lab.infrastructure.qwen_client import QwenTTSClient
from tts_lab.domain.entities import TTSRequest

# Define emotions
emotions = {
    "happy": "Habla con mucha alegría y entusiasmo",
    "sad": "Habla con tono melancólico y suave",
    "excited": "Habla muy emocionado y rápido",
    "calm": "Habla con tono tranquilo y relajado",
}

text = "Hoy es un día especial."

with QwenTTSClient(device="mps") as client:
    for emotion_name, instruct in emotions.items():
        print(f"Generating {emotion_name} version...")
        
        request = TTSRequest(
            text=text,
            language="Spanish",
            speaker="Serena",
            instruct=instruct
        )
        
        audio = client.generate(request)
        
        filename = f"emotion_{emotion_name}.wav"
        with open(f"output/{filename}", "wb") as f:
            f.write(audio.audio_data)
        
        print(f"  → output/{filename}")

print("All emotions generated!")
```

---

## Example 7: Multi-Language Generation

```python
from tts_lab.infrastructure.qwen_client import QwenTTSClient
from tts_lab.domain.entities import TTSRequest

# Text in different languages
texts = {
    "Spanish": "Hola, ¿cómo estás?",
    "English": "Hello, how are you?",
    "French": "Bonjour, comment allez-vous?",
    "German": "Hallo, wie geht es dir?",
    "Portuguese": "Olá, como você está?",
}

with QwenTTSClient(device="mps") as client:
    for language, text in texts.items():
        print(f"Generating in {language}...")
        
        request = TTSRequest(
            text=text,
            language=language
        )
        
        audio = client.generate(request)
        
        filename = f"language_{language.lower()}.wav"
        with open(f"output/{filename}", "wb") as f:
            f.write(audio.audio_data)
        
        print(f"  → output/{filename}")

print("All languages generated!")
```

---

## Example 8: Process Audio Reference

```python
import soundfile as sf
import noisereduce as nr
from pathlib import Path

# Load reference audio
audio_path = "voice_profiles/felipe/reference_raw.wav"
audio, sr = sf.read(audio_path)

# Reduce noise
print("Reducing noise...")
reduced_noise = nr.reduce_noise(y=audio, sr=sr)

# Normalize
print("Normalizing...")
max_val = max(abs(reduced_noise))
normalized = reduced_noise / max_val * 0.95

# Save processed
output_path = "voice_profiles/felipe/reference_clean.wav"
sf.write(output_path, normalized, sr)

print(f"Processed audio saved to: {output_path}")

# Verify
info = sf.info(output_path)
print(f"Duration: {info.duration:.2f}s")
print(f"Sample rate: {info.samplerate} Hz")
print(f"Channels: {info.channels}")
```

---

## Example 9: Test Voice Profile Quality

```python
from tts_lab.infrastructure.qwen_client import QwenTTSClient
from tts_lab.domain.entities import VoiceProfile

def test_voice_profile(profile_path: str, test_texts: list[str]):
    """Test voice profile with multiple texts."""
    
    profile = VoiceProfile(
        name="test",
        reference_audio_path=profile_path,
        reference_text="Reference text here..."
    )
    
    with QwenTTSClient(device="mps") as client:
        for i, text in enumerate(test_texts):
            print(f"Test {i+1}: {text[:30]}...")
            
            try:
                audio = client.clone_voice(profile, text)
                
                filename = f"test_{i+1:02d}.wav"
                with open(f"output/tests/{filename}", "wb") as f:
                    f.write(audio.audio_data)
                
                print(f"  ✓ Duration: {audio.duration_seconds:.2f}s")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")

# Run tests
test_texts = [
    "Esta es una prueba corta.",
    "Esta es una prueba más larga para verificar que el modelo puede manejar textos de diferentes longitudes sin problemas.",
    "¿Puede manejar preguntas?",
    "¡Y exclamaciones también!",
]

test_voice_profile(
    "voice_profiles/felipe/reference_v2.wav",
    test_texts
)
```

---

## Example 10: Create Voice Profile from Recording

```python
import subprocess
from pathlib import Path

def record_voice_profile(name: str, duration: int = 15):
    """Record new voice profile."""
    
    profile_dir = Path(f"voice_profiles/{name}")
    profile_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = profile_dir / "reference.wav"
    
    print(f"Recording voice profile for '{name}'...")
    print(f"Duration: {duration} seconds")
    print("Speak clearly and naturally...")
    
    # Record using sox
    cmd = [
        "sox",
        "-t", "coreaudio", "Micrófono de iPhone 13 mini",
        "-r", "24000",
        "-c", "1",
        "-b", "16",
        str(output_file),
        "trim", "0", str(duration)
    ]
    
    subprocess.run(cmd, check=True)
    
    print(f"✓ Recorded: {output_file}")
    
    # Create metadata
    metadata = {
        "name": name,
        "description": f"Voice profile for {name}",
        "language": "Spanish",
        "reference_audio": "reference.wav",
        "reference_text": "La tecnología de inteligencia artificial...",
    }
    
    import json
    metadata_file = profile_dir / "metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))
    
    print(f"✓ Metadata: {metadata_file}")
    
    return str(output_file)

# Record new profile
record_voice_profile("felipe_v3", duration=15)
```

---

## Common Patterns

### Pattern 1: Context Manager

Always use context manager for automatic cleanup:

```python
# ✅ Good
with QwenTTSClient(device="mps") as client:
    audio = client.generate(request)

# ❌ Bad
client = QwenTTSClient(device="mps")
audio = client.generate(request)
# Memory leak - model not unloaded
```

### Pattern 2: Error Handling

```python
from tts_lab.domain.exceptions import TTSError, VoiceProfileError

try:
    with QwenTTSClient(device="mps") as client:
        audio = client.clone_voice(profile, text)
except VoiceProfileError as e:
    print(f"Profile error: {e}")
except TTSError as e:
    print(f"TTS error: {e}")
```

### Pattern 3: Progress Feedback

```python
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    console=console,
) as progress:
    task = progress.add_task("Generating audio...", total=None)
    
    with QwenTTSClient(device="mps") as client:
        audio = client.generate(request)
    
    progress.update(task, completed=True)
    console.print("[green]✓[/green] Audio generated!")
```

---

**Version:** 1.0.0
**Last Updated:** 2026-03-12
