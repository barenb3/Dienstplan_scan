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

# Datei suchen
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

# Schichtzeiten definieren
schichtzeiten = {
    "F14": ("07:00", "10:00"),
    "F06": ("07:00", "14:00"),
    "F13": ("07:00", "10:30"),
    "S04": ("13:45", "20:30"),
    "F01": ("06:45", "14:00"),
}

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

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    kalender = Calendar()
    letzter_tag = []

    tag_pattern = r"(\d{1,2})\s+(Mo|Di|Mi|Do|Fr|Sa|So)"
    code_pattern = r"\b(F\d{2}|S\d{2})\b"

    for line in lines:
        tag_matches = re.findall(tag_pattern, line)
        if tag_matches:
            letzter_tag = [int(t[0]) for t in tag_matches]
        else:
            code_matches = re.findall(code_pattern, line)
            code_matches = [normalize(c) for c in code_matches if normalize(c) in schichtzeiten]
            for tag, code in zip(letzter_tag, code_matches):
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
            letzter_tag = []

    with open(ics_ziel, "w", encoding="utf-8") as f:
        f.writelines(kalender.serialize_iter())

    print(f"✅ Dienstplan gespeichert als: {ics_ziel}")

if __name__ == "__main__":
    verarbeite_bild()
