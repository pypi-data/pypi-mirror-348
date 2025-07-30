import librosa
import os

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def analyze_audio(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError("Arquivo não encontrado.")

    y, sr = librosa.load(filepath)

    # BPM
    tempo = librosa.beat.tempo(y=y, sr=sr)[0]

    # CQT (Constant-Q Transform) pra análise de tom
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_avg = chroma.mean(axis=1)
    note_idx = chroma_avg.argmax()

    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    note = note_names[note_idx]

    # Heurística simples pra determinar se é maior ou menor
    major_likelihood = chroma[4].mean() + chroma[11].mean()
    minor_likelihood = chroma[3].mean() + chroma[10].mean()
    mode = "minor" if minor_likelihood > major_likelihood else "major"

    return round(tempo), note, mode
if __name__ == "__main__":
    # Altere o nome abaixo pro nome do seu beat
    filepath = "sua_musica.wav"

    bpm, note, mode = analyze_audio(filepath)
    print(f"BPM: {bpm}")
    print(f"Key: {note} {mode}")
