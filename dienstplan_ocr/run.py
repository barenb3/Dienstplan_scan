import pytesseract
from PIL import Image
import re
from datetime import datetime
from ics import Calendar, Event
import os
import uuid
from calendar import monthrange

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
    code = code.replace("O", "0").replace("o", "0").replace(" ", "").strip().upper()
    # Smart fix: häufige OCR-Fehler
    if code in {"FO6", "F0G", "F0G", "F0O", "F06"}:
        return "F06"
    return code

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

    belegte_tage = set()
    dienst_pro_tag = {}

    tag_buffer = []
    for idx, line in enumerate(lines):
        if tag_pattern.match(line):
            tag = int(tag_pattern.match(line).group(1))
            tag_buffer.append((idx, tag))

    for idx, tag in tag_buffer:
        if tag in dienst_pro_tag:
            continue
        for offset in range(1, 6):  # bis zu 5 Zeilen nach unten schauen
            if idx + offset < len(lines):
                candidate = normalize(lines[idx + offset])
                if candidate in schichtzeiten and candidate not in irrelevante:
                    dienst_pro_tag[tag] = candidate
                    belegte_tage.add(tag)
                    break

    _, max_tage = monthrange(jahr, monat)
    alle_tage = set(range(1, max_tage + 1))
    freie_tage = sorted(alle_tage - belegte_tage)

    for tag, code in dienst_pro_tag.items():
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

    for tag in freie_tage:
        datum = datetime(jahr, monat, tag)
        event = Event()
        event.name = "Frei"
        event.begin = datum.replace(hour=0, minute=0)
        event.end = datum.replace(hour=23, minute=59)
        event.uid = f"{uuid.uuid4()}@frei.org"
        kalender.events.add(event)
        print(f"➕ {datum.strftime('%d.%m.%Y')}: Frei")

    with open(ics_ziel, "w", encoding="utf-8") as f:
        f.writelines(kalender.serialize_iter())

    print(f"✅ Dienstplan gespeichert als: {ics_ziel}")

if __name__ == "__main__":
    verarbeite_bild()
