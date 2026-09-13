# TTS Lab Architecture Details

## Clean Architecture Layers

### Domain Layer (Pure)

**Purpose:** Define business logic without external dependencies.

**Components:**

1. **Entities** (`domain/entities.py`)
   - `TTSRequest`: Immutable data structure for TTS requests
   - `AudioResult`: Immutable audio output
   - `VoiceProfile`: Voice cloning reference

2. **Protocols** (`domain/protocols.py`)
   - `TTSClient`: Interface for TTS generation
   - `AudioRepository`: Interface for audio storage

3. **Exceptions** (`domain/exceptions.py`)
   - `TTSError`: Base exception
   - `VoiceProfileError`: Profile validation errors
   - `ModelLoadError`: Model loading failures
   - `AudioFormatError`: Format validation errors

**Key Principle:** Zero external dependencies. Only Python stdlib.

---

### Application Layer (Orchestration)

**Purpose:** Coordinate domain logic and delegate side effects.

**Components:**

1. **Use Cases** (`application/use_cases.py`)
   - `GenerateSpeechUseCase`: Main orchestration logic

2. **DTOs** (`application/dto.py`)
   - `GenerateSpeechRequest`: Input data
   - `GenerateSpeechResponse`: Output data

**Key Principle:** Pure orchestration, no direct side effects.

---

### Infrastructure Layer (Impure)

**Purpose:** Handle all external interactions.

**Components:**

1. **QwenTTSClient** (`infrastructure/qwen_client.py`)
   - Model loading (lazy)
   - Inference execution
   - Audio conversion

2. **FileAudioRepository** (`infrastructure/file_storage.py`)
   - File I/O operations
   - Security sanitization
   - Content hashing

3. **Config** (`infrastructure/config.py`)
   - Environment variables
   - Default values

**Key Principle:** Isolate all side effects here.

---

## Data Flow

### Generate Speech Flow

```
User Request
    ↓
CLI (Typer)
    ↓
GenerateSpeechRequest (DTO)
    ↓
GenerateSpeechUseCase.execute()
    ↓
TTSRequest (Domain Entity)
    ↓
QwenTTSClient.generate()
    ↓
AudioResult (Domain Entity)
    ↓
FileAudioRepository.save_with_hash()
    ↓
GenerateSpeechResponse (DTO)
    ↓
User receives audio path
```

### Clone Voice Flow

```
User Request
    ↓
CLI (Typer)
    ↓
VoiceProfile (Domain Entity)
    ↓
QwenTTSClient.clone_voice()
    ├─ Validate profile
    ├─ Load reference audio
    ├─ Generate clone
    └─ Convert to AudioResult
    ↓
FileAudioRepository.save()
    ↓
User receives cloned audio
```

---

## Design Patterns Used

### 1. Repository Pattern

**Purpose:** Abstract data persistence.

```python
class AudioRepository(Protocol):
    def save(self, audio: AudioResult, filename: str) -> str: ...
    def load(self, path: str) -> AudioResult: ...
```

**Benefit:** Can swap FileAudioRepository for S3AudioRepository, etc.

---

### 2. Context Manager Pattern

**Purpose:** Resource management.

```python
with QwenTTSClient(...) as client:
    audio = client.generate(request)
# Auto cleanup on exit
```

**Benefit:** Guaranteed resource cleanup.

---

### 3. Lazy Loading Pattern

**Purpose:** Defer expensive operations.

```python
def _ensure_model_loaded(self):
    if self._model is None:
        self._model = load_heavy_model()
```

**Benefit:** Load model only when needed.

---

### 4. Content-Addressable Storage

**Purpose:** Unique, reproducible filenames.

```python
hash_input = f"{text}_{language}".encode()
content_hash = hashlib.sha256(hash_input).hexdigest()[:12]
filename = f"speech_{content_hash}.wav"
```

**Benefit:** Cache-friendly, no duplicates.

---

## Security Considerations

### Path Traversal Prevention

```python
def _sanitize_filename(self, filename: str) -> str:
    # Remove path separators
    safe = Path(filename).name
    # Ensure valid extension
    if not safe.endswith(".wav"):
        safe = f"{safe}.wav"
    return safe

def _validate_path(self, path: str) -> Path:
    resolved = Path(path).resolve()
    if not str(resolved).startswith(str(self._output_dir)):
        raise ValueError(f"Path traversal detected: {path}")
    return resolved
```

### Input Validation

```python
def _validate_voice_profile(self, profile: VoiceProfile) -> None:
    ref_path = Path(profile.reference_audio_path)
    if not ref_path.exists():
        raise VoiceProfileError(f"Reference audio not found: {ref_path}")
    if ref_path.suffix.lower() not in [".wav", ".mp3", ".flac"]:
        raise VoiceProfileError(f"Unsupported audio format: {ref_path.suffix}")
```

---

## Testing Strategy

### Unit Tests

**Domain Layer:**
- Test entities immutability
- Test protocol compliance
- Test exception hierarchy

**Application Layer:**
- Mock TTSClient and AudioRepository
- Test orchestration logic
- Test DTO validation

**Infrastructure Layer:**
- Mock model loading
- Test file operations
- Test security validations

### Integration Tests

**End-to-End:**
- Load real model
- Generate real audio
- Verify audio quality

---

## Performance Considerations

### Model Loading

- **Lazy loading:** Load only when needed
- **Context manager:** Unload when done
- **Memory management:** Clear GPU cache

### File Operations

- **Buffered I/O:** Use BytesIO for in-memory operations
- **Content hashing:** Avoid regenerating same content
- **Path validation:** Single validation per operation

### Inference

- **Device selection:** MPS > CUDA > CPU
- **Batch processing:** Generate multiple audios in one session
- **Streaming:** Not supported yet (future work)

---

## Extension Points

### Add New TTS Provider

1. Implement `TTSClient` protocol
2. Add to infrastructure layer
3. Update CLI to support provider selection

### Add New Storage Backend

1. Implement `AudioRepository` protocol
2. Add to infrastructure layer
3. Update config with backend selection

### Add New Use Case

1. Create new use case in application layer
2. Define request/response DTOs
3. Add CLI command

---

## Known Limitations

1. **Latency:** 30-40s for voice cloning without flash-attn
2. **Memory:** Model requires ~4GB RAM
3. **Streaming:** Not supported (generates complete audio)
4. **Languages:** Limited to 10 supported languages
5. **Reference quality:** Requires clean 10-15s audio

---

## Future Improvements

1. **Streaming support:** Chunk-by-chunk generation
2. **Flash-attention:** Reduce latency to 10s
3. **Caching:** Cache model in memory for repeated use
4. **API server:** FastAPI wrapper for HTTP access
5. **Batch API:** Generate multiple audios in parallel
6. **Voice mixer:** Combine characteristics from multiple voices
7. **Quality metrics:** Automated audio quality scoring

---

**Version:** 1.0.0
**Last Updated:** 2026-03-12
