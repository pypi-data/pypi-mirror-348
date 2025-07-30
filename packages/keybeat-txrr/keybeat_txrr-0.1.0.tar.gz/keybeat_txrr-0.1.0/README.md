# KeyBeat 🎧🎹

**KeyBeat** é uma biblioteca Python para detectar o **BPM** (batidas por minuto) e o **tom musical** (incluindo se é **maior** ou **menor**) de arquivos de áudio (`.mp3`, `.wav`, `.flac`).

## Como usar

```python
from keybeat import analyze_audio

bpm, key, mode = analyze_audio("minha_musica.wav")
print(f"BPM: {bpm}")
print(f"Tom: {key} ({mode})")
