#!/bin/bash

# Interrompe lo script in caso di errore
set -e

echo "Inizio il setup virtuale per Reachy Mini..."
echo "----------------------------------------------------"

# 1. Individua Python esattamente alla versione 3.12
echo "Ricerca di Python 3.12 nel sistema..."
PYTHON_CMD=""
for candidate in python3.12 python3 python py; do
    if command -v "$candidate" &> /dev/null; then
        _major=$("$candidate" -c 'import sys; print(sys.version_info.major)' 2>/dev/null)
        _minor=$("$candidate" -c 'import sys; print(sys.version_info.minor)' 2>/dev/null)
        if [ "$_major" -eq 3 ] && [ "$_minor" -eq 12 ]; then
            PYTHON_CMD="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "Errore: Python 3.12 non trovato (versioni diverse non sono accettate)."
    echo "Assicurati di aver installato esattamente Python 3.12 e che sia nel PATH."
    exit 1
fi

PY_FULL_VERSION=$("$PYTHON_CMD" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
echo "Trovato Python $PY_FULL_VERSION (comando: $PYTHON_CMD)"

# 2. Creazione dell'ambiente virtuale con Python 3.12
echo "Creazione dell'ambiente virtuale (.venv) con Python 3.12..."
"$PYTHON_CMD" -m venv .venv
source .venv/bin/activate

# 3. Creazione del file requirements.txt
echo "Creazione del file requirements.txt..."
cat << 'EOF' > requirements.txt
pygame
reachy-mini[mujoco]
EOF

# 4. Installazione delle dipendenze da requirements.txt
# Nota: Viene installato l'SDK con il tag [mujoco] necessario per la simulazione
echo "Installazione delle dipendenze da requirements.txt (potrebbe volerci un minuto)..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# 5. Pre-download dei dataset di movimenti da HuggingFace
echo "Download delle librerie di movimenti da HuggingFace (emotions + dances)..."
echo "Questo passaggio potrebbe richiedere qualche minuto alla prima esecuzione."
python -c "
from reachy_mini.motion.recorded_move import RecordedMoves
print('  -> Scarico emotions-library...')
RecordedMoves('pollen-robotics/reachy-mini-emotions-library')
print('  -> Scarico dances-library...')
RecordedMoves('pollen-robotics/reachy-mini-dances-library')
print('  -> Dataset salvati in cache locale.')
" || echo "Attenzione: download dei dataset fallito (controlla la connessione). Verranno scaricati al primo avvio."

# 6. Download del file audio di esempio da Google Drive
echo "Download del file audio di esempio (sample_audio.mp3) da Google Drive..."
GDRIVE_FILE_ID="1mqqGW85aRCHemKuzGWddWGbTZ7K2M-s-"
AUDIO_FILE="sample_audio.mp3"
GDRIVE_URL="https://drive.usercontent.google.com/download?id=${GDRIVE_FILE_ID}&export=download&confirm=t"

if [ ! -f "$AUDIO_FILE" ]; then
    if command -v curl &> /dev/null; then
        curl -L -o "$AUDIO_FILE" "$GDRIVE_URL" \
            && echo "  -> Audio scaricato correttamente." \
            || echo "Attenzione: download audio fallito. Scarica manualmente '$AUDIO_FILE'."
    elif command -v wget &> /dev/null; then
        wget -O "$AUDIO_FILE" "$GDRIVE_URL" \
            && echo "  -> Audio scaricato correttamente." \
            || echo "Attenzione: download audio fallito. Scarica manualmente '$AUDIO_FILE'."
    else
        echo "Attenzione: ne' curl ne' wget trovati. Scarica manualmente '$AUDIO_FILE'."
    fi
else
    echo "  -> File '$AUDIO_FILE' gia' presente, salto il download."
fi

# 7. Creazione del primo script di test Python
echo "Creazione dello script di test 'hello_reachy.py'..."
cat << 'EOF' > hello_reachy.py
from reachy_mini import ReachyMini
from reachy_mini.motion.recorded_move import RecordedMoves
import time
import pygame

# Pre-carica le librerie di movimenti
emotions = RecordedMoves("pollen-robotics/reachy-mini-emotions-library")
dances   = RecordedMoves("pollen-robotics/reachy-mini-dances-library")

# CON QUESTE DUE LINEE DI CODICE POTETE VISUALIZZARE TUTTE LE ANIMAZIONI DEL ROBOT
print(emotions.list_moves())
print(dances.list_moves())

print("Connessione a Reachy Mini in simulazione...")
pygame.mixer.init()

# DICHIARAZIONE DELLA FUNZIONE PER RIPRODURRE AUDIO
def play_sound(file_path: str):
    # Carica il file audio (inserisci il percorso corretto del tuo file)
    pygame.mixer.music.load(file_path)
    
    # Avvia la riproduzione
    pygame.mixer.music.play()

    print("Riproduzione in corso...")

    # Mantieni il programma in esecuzione finché l'audio non finisce
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    print("Riproduzione terminata.")

# QUI, SOTTO QUESTO COMMENTO, INSERITE LE VOSTRE FUNZIONI


with ReachyMini() as mini:
    # DA QUI IN POI SCRIVETE IL CODICE DEL PROGETTO

    # IL CODICE SOTTO QUESTO COMMENTO DEVE ESSERE SOSTITUITO CON IL CODICE DEL PROGETTO
    print("Connesso! Inizio la sequenza di test...")

    input("Premi INVIO per muovere le antenne")
    
    # Muove le antenne
    mini.goto_target(antennas=[0.5, -0.5], duration=0.5)
    time.sleep(0.5)
    mini.goto_target(antennas=[-0.5, 0.5], duration=0.5)
    time.sleep(0.5)
    
    # Riporta le antenne in posizione neutra
    mini.goto_target(antennas=[0.0, 0.0], duration=0.5)

    input("Premi INVIO per riprodurre un audio")
    
    # ESEMPIO DI COME RIPRODURRE UN AUDIO
    play_sound("sample_audio.mp3")

    input("Premi INVIO per riprodurre un'animazione")
    
    # ESEMPIO DI COME RIPRODURRE UN'ANIMAZIONE
    move = emotions.get("dance3")   # <-- sostituisci con il nome che vuoi tu
    mini.play_move(move)

    
    print("Test completato con successo!")


    # QUI TERMINA IL CODICE DEL PROGETTO
EOF

echo ""
echo "Setup completato con successo!"
echo "----------------------------------------------------"
echo "Per avviare la simulazione, apri DUE terminali separati."
echo ""
echo "TERMINALE 1 (Il Demone della Simulazione):"
echo "  source .venv/bin/activate"
echo "  mjpython .venv/bin/reachy-mini-daemon --sim"
echo "  # NOTA: su macOS usare mjpython (richiesto da MuJoCo)"
echo ""
echo "TERMINALE 2 (Il tuo Codice):"
echo "  source .venv/bin/activate"
echo "  python hello_reachy.py"
echo "----------------------------------------------------"