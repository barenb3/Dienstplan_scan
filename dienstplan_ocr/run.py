import pytesseract
from PIL import Image
import re
from datetime import datetime
from ics import Calendar, Event
import os
import uuid

os.environ["TESSDATA_PREFIX"] = "/usr/share/tessdata"

verzeichnis = "/config/www/"
dienstplan_datei = None
monat = jahr = None

muster = re.compile(r"dienstplan_(\d{2})\.(\d{4})\.jpg")
for datei in os.listdir(verzeichnis):
    match = muster.match(datei)
    if match:
        monat = int(match.group(1))
        jahr = int(match.group(2))
        dienstplan_datei = os.path.join(verzeichnis, datei)
        break

if not dienstplan_datei:
    print("❌ Kein Dienstplanbild gefunden.")
    exit(1)

ics_ziel = os.path.join(verzeichnis, f"dienstplan_{monat:02d}.{jahr}.ics")

schichtzeiten = {
    "F14": ("07:00", "10:00"),
    "F06": ("07:00", "14:00"),
    "F13": ("07:00", "10:30"),
    "S04": ("13:45", "20:30"),
    "F01": ("06:45", "14:00"),
}

irrelevante = {"W", "WFREI", "FREI", "Wfrei", "i", "I"}

def normalize(code):
    return code.replace("O", "0").replace("o", "0").strip().upper()

def verarbeite_bild():
    print(f"📷 Verarbeite Datei: {dienstplan_datei}")
    bild = Image.open(dienstplan_datei)
    text = pytesseract.image_to_string(bild, lang="deu")

    print("\n🔍 OCR-TEXT:")
    print("-" * 30)
    print(text)
    print("-" * 30 + "\n")

    kalender = Calendar()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    tag_pattern = re.compile(r"^(\d{1,2})\s*(Mo|Di|Mi|Do|Fr|Sa|So)?$")
    code_pattern = re.compile(r"^(F\d{2}|S\d{2})$")

    tag_code_pairs = []
    tag_buffer = []

    # 1. Erfasse alle Tage mit Position
    for idx, line in enumerate(lines):
        if tag_pattern.match(line):
            tag = int(tag_pattern.match(line).group(1))
            tag_buffer.append((idx, tag))

    # 2. Für jeden erkannten Tag: Suche in den nächsten 3 Zeilen nach Schichtcode
    for idx, tag in tag_buffer:
        for offset in range(1, 4):
            if idx + offset < len(lines):
                candidate = normalize(lines[idx + offset])
                if candidate in schichtzeiten and candidate not in irrelevante:
                    tag_code_pairs.append((tag, candidate))
                    break

    # 3. Erzeuge Kalendereinträge
    for tag, code in tag_code_pairs:
        try:
            datum = datetime(jahr, monat, tag)
            start, ende = schichtzeiten[code]
            start_dt = datetime.strptime(f"{datum.date()} {start}", "%Y-%m-%d %H:%M")
            ende_dt = datetime.strptime(f"{datum.date()} {ende}", "%Y-%m-%d %H:%M")
            event = Event()
            event.name = f"Dienst: {code}"
            event.begin = start_dt
            event.end = ende_dt
            event.uid = f"{uuid.uuid4()}@{str(uuid.uuid4())[:4]}.org"
            kalender.events.add(event)
            print(f"➕ {datum.strftime('%d.%m.%Y')}: Dienst {code} ({start}–{ende})")
        except Exception as e:
            print(f"⚠️ Fehler bei Tag {tag}: {e}")

    with open(ics_ziel, "w", encoding="utf-8") as f:
        f.writelines(kalender.serialize_iter())

    print(f"✅ Dienstplan gespeichert als: {ics_ziel}")

if __name__ == "__main__":
    verarbeite_bild()
