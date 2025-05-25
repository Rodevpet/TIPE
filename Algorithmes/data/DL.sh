#!/bin/zsh

# Vérifie si un argument (URL) a été fourni
if [ -z "$1" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

# Récupère l'URL fournie en argument
URL=$1

# Télécharge la playlist
pytube $URL

first_subdir=$(ls -d */ | head -n 1)
cd $first_subdir
# Convertit tout en .wav
for f in *.mp4; do
    ffmpeg -i "$f" -q:a 0 -map a -ac 1 "${f%.mp4}.wav"
    rm "${f%.mp4}"
done


# Nom du fichier d'entrée
for f in *.wav; do
    input_file="$f.wav"

    # Obtenir la durée totale du fichier audio
    duration=$(ffmpeg -i "$input_file" 2>&1 | grep "Duration" | awk '{print $2}' | tr -d ,)
    duration_seconds=$(echo "$duration" | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }')

    # Calculer le nombre de segments de 2 secondes
    num_segments=$((duration_seconds / 2))

    # Découper le fichier audio en segments de 2 secondes
    for i in $(seq 0 $num_segments); do
        start_time=$((i * 2))
        output_file="segment_${i}.wav"
        ffmpeg -i "$input_file" -ss $start_time -t 2 -c copy "/Users/robin/Scolaire/CPGE/TIPE/Algorithmes/Témoins/$output_file"
    done
done


mv * ..

# Supprimer le dossier courant
cd ..
rmdir $first_subdir

