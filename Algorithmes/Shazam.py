from ChemPlot import*
from scipy import fft, signal
import scipy
from scipy.io.wavfile import read
import glob
from typing import List, Dict, Tuple
from tqdm import tqdm
import pickle

def create_constellation(audio, Fs):
    # Parameters
    Intervalle = 3 #en seconde
    Nbre_point = int(Intervalle * Fs)
    Nbre_point += Nbre_point % 2
    num_peaks = 15

    # Pad the song to divide evenly into windows
    amount_to_pad = Nbre_point - audio.size % Nbre_point

    song_input = np.pad(audio, (0, amount_to_pad))

    # Perform a short time fourier transform
    frequencies, times, stft = signal.stft(
        song_input, Fs, nperseg=Nbre_point, nfft=Nbre_point, return_onesided=True
    )

    constellation_map = []

    for time_idx, window in enumerate(stft.T):
        # Spectrum is by default complex.
        # We want real values only
        spectrum = abs(window)
        # Find peaks - these correspond to interesting features
        # Note the distance - want an even spread across the spectrum
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=2000)

        # Only want the most prominent peaks
        # With a maximum of 15 per time slice
        n_peaks = min(num_peaks, len(peaks))
        # Get the n_peaks largest peaks from the prominences
        # This is an argpartition
        # Useful explanation: https://kanoki.org/2020/01/14/find-k-smallest-and-largest-values-and-its-indices-in-a-numpy-array/
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map.append([time_idx, frequency])

    return constellation_map

def create_hashes(constellation_map, song_id=None):
    hashes = {}
    # Utiliser cette valeur pour l'échantillonnage - 23_000 est légèrement supérieur à la valeur maximale.
    # fréquence pouvant être stockée dans les fichiers .wav, 22,05 kHz
    frequence_max = 23_000
    nbre_bits_frequence = 10
    occurrence_hash = {}
    # Itération des données
    for idx, (time, freq) in enumerate(constellation_map):
        # Itère les 60 paires (temps,fréquence) pour produire les hachages combinatoires
        # La constellation est déjà triée selon le temps
        # Cela permet donc de trouver les n points suivants dans le temps (bien qu'ils puissent se produire en même temps)
        for prochain_temps, prochaine_frequence in constellation_map[idx : idx + 60]: # Pour <60 paires, le hashage diminue car de plus en plus de données se ressembles.
            diff = prochain_temps - time
            # Si la différence de temps entre les paires est trop grande ou trop petite, on ignore l'ensemble. C'est contre-intuitif car on pourrait se dire que si l'on divise en plus petit groupe, on aura plus de hash, mais le manque de valeurs fait que l'on aura plus de hash identique.
            if diff <= 1 or diff > 10:
                continue

            # Convertis la fréquence en 1024 bits
            freq_binned = freq / frequence_max * (2 ** nbre_bits_frequence)
            other_freq_binned = prochaine_frequence / frequence_max * (2 ** nbre_bits_frequence)

            # Production d'un hash à 32 bits
            # Utiliser le décalage de bits pour déplacer les bits à l'emplacement correct
            hash = int(freq_binned) | (int(other_freq_binned) << 10) | (int(diff) << 20)
            if (hash in hashes):
                if (hash in occurrence_hash):
                    occurrence_hash[hash] += 1
                else :
                    occurrence_hash[hash] =0
            hashes[hash] = (time, song_id)
    return hashes,occurrence_hash



print("Erreur ici")
songs = glob.glob('data/*.wav')
print("Erreur ici")
song_name_index = {}
database: Dict[int, List[Tuple[int, int]]] = {}
print("Erreur ici")
# Go through each song, using where they are alphabetically as an id
for index, filename in enumerate(tqdm(sorted(songs))):
    print(filename)
    song_name_index[index] = filename
    # Read the song, create a constellation and hashes
    Fs, audio_input = read(filename)
    constellation = create_constellation(audio_input, Fs)
    (hashes,_) = create_hashes(constellation, index)

    # For each hash, append it to the list for this hash
    for hash, time_index_pair in hashes.items():
        if hash not in database:
            database[hash] = []
        # Comprend comme : Ajouter à la base de donnée, a l'id Hash : [Emplacement temporel du Hash, Id du song]
        database[hash].append(time_index_pair)
print("Erreur ici")
# Dump the database and list of songs as pickles
with open("database.pickle", 'w') as db:
    pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)
with open("song_index.pickle", 'w') as songs:
    pickle.dump(song_name_index, songs, pickle.HIGHEST_PROTOCOL)