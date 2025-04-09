import pytesseract
from PIL import Image
import re
from datetime import datetime
from ics import Calendar, Event
import os

bildpfad = "/config/www/dienstplan.jpg"
ics_ziel = "/config/www/dienstplan.ics"

schichtzeiten = {
    "F14": ("07:00", "10:00"),
    "F06": ("07:00", "14:00"),
    "F13": ("07:00", "10:30"),
    "S04": ("13:45", "20:30"),
    "F01": ("06:45", "14:00"),
}

monat = 4
jahr = 2025

def verarbeite_bild():
    if not os.path.exists(bildpfad):
        print("❌ Kein Bild gefunden unter:", bildpfad)
        return

    bild = Image.open(bildpfad)
    text = pytesseract.image_to_string(bild, lang="deu")
    kalender = Calendar()

    tag_pattern = re.compile(r"(\d{1,2})\s+\w+\s+([A-Z0-9]+)")

    for zeile in text.splitlines():
        match = tag_pattern.search(zeile)
        if match:
            tag = int(match.group(1))
            code = match.group(2).upper()
            zeiten = schichtzeiten.get(code)
            if zeiten:
                datum = datetime(jahr, monat, tag)
                start = datetime.strptime(f"{datum.date()} {zeiten[0]}", "%Y-%m-%d %H:%M")
                ende = datetime.strptime(f"{datum.date()} {zeiten[1]}", "%Y-%m-%d %H:%M")
                event = Event()
                event.name = f"Dienst: {code}"
                event.begin = start
                event.end = ende
                kalender.events.add(event)

    with open(ics_ziel, "w", encoding="utf-8") as f:
        f.writelines(kalender.serialize_iter())

    print("✅ Dienstplan geschrieben nach:", ics_ziel)

verarbeite_bild()
