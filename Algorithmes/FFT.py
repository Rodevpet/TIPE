import librosa
import numpy as np
from scipy.spatial.distance import euclidean
import os
import plotly.graph_objects as go

# Fonction pour segmenter un fichier audio en segments de durée fixe
def segment_audio(file_path, segment_length=4):
    y, sr = librosa.load(file_path)
    segment_samples = segment_length * sr
    segments = [y[i:i + segment_samples] for i in range(0, len(y) - segment_samples + 1, segment_samples)]
    return segments, sr

# Fonction pour calculer la Transformée de Fourier d'un segment
def calculate_fft(segment, sr):
    return np.fft.fft(segment)

# Fonction pour comparer deux spectres de Fourier
def compare_fft(fft1, fft2):
    return euclidean(np.abs(fft1), np.abs(fft2))

# Chemin vers le dossier contenant les fichiers audio
audio_dir = './data'

# Liste pour stocker les fichiers audio
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]

# Liste pour stocker les résultats
results = []

# Comparer les segments de tous les fichiers audio
for i, file_path1 in enumerate(audio_files):
    segments1, sr1 = segment_audio(file_path1)
    for j, file_path2 in enumerate(audio_files[i+1:], start=i+1):
        segments2, sr2 = segment_audio(file_path2)
        for k, segment1 in enumerate(segments1):
            fft1 = calculate_fft(segment1, sr1)
            for l, segment2 in enumerate(segments2):
                if l < len(segments2):  # Vérification pour éviter les indices invalides
                    fft2 = calculate_fft(segment2, sr2)
                    distance = compare_fft(fft1, fft2)
                    results.append((distance, file_path1, file_path2, k, l))

# Trier les résultats par distance
results.sort(key=lambda x: x[0])
print(results)
"""
# Afficher les 5 paires de segments les plus similaires
for idx, (distance, file_path1, file_path2, k, l) in enumerate(results[:5]):
    try:
        print(f"Paire {idx + 1}: Segment {k} de {file_path1} et segment {l} de {file_path2}, Distance: {distance}")

        # Calculer les fréquences correspondantes
        freqs1 = np.fft.fftfreq(len(segments1[k]), 1/sr1)[:len(segments1[k])//2]
        freqs2 = np.fft.fftfreq(len(segments2[l]), 1/sr2)[:len(segments2[l])//2]

        # Limiter les fréquences à 44000 Hz
        mask1 = freqs1 <= 44000
        mask2 = freqs2 <= 44000

        # Tracer les spectres de fréquence avec Plotly
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=freqs1[mask1],
                y=np.abs(calculate_fft(segments1[k], sr1)[:len(segments1[k])//2][mask1]),
                mode='lines',
                name=f"Segment {k} de {os.path.basename(file_path1)}",
                line=dict(color='blue', width=2),
                opacity=0.5
            )
        )

        fig.add_trace(
            go.Scatter(
                x=freqs2[mask2],
                y=np.abs(calculate_fft(segments2[l], sr2)[:len(segments2[l])//2][mask2]),
                mode='lines',
                name=f"Segment {l} de {os.path.basename(file_path2)}",
                line=dict(color='red', width=2),
                opacity=0.5
            )
        )

        fig.update_layout(
            title=f"Comparaison des spectres de fréquence (Paire {idx + 1})",
            xaxis_title="Fréquence (Hz)",
            yaxis_title="Amplitude",
            showlegend=True
        )

        fig.show(renderer="browser")  # Ouvrir le graphique dans le navigateur
"""