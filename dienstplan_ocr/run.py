import pytesseract
from PIL import Image
import re
from datetime import datetime
from ics import Calendar, Event
import os

os.environ["TESSDATA_PREFIX"] = "/usr/share/tessdata"

print("📂 Inhalt von /usr/share/tessdata/:")
os.system("ls -l /usr/share/tessdata/")

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
    print("❌ Keine passende Dienstplan-Datei gefunden (Format: dienstplan_MM.JJJJ.jpg)")
    exit(1)

ics_ziel = os.path.join(verzeichnis, f"dienstplan_{monat:02d}.{jahr}.ics")

schichtzeiten = {
    "F14": ("07:00", "10:00"),
    "F06": ("07:00", "14:00"),
    "F13": ("07:00", "10:30"),
    "S04": ("13:45", "20:30"),
    "F01": ("06:45", "14:00"),
}

def normalize_code(code):
    return (
        code.replace("O", "0")
            .replace("o", "0")
            .replace(" ", "")
            .strip()
            .upper()
    )

def verarbeite_bild():
    print(f"📷 Verarbeite Datei: {dienstplan_datei}")
    bild = Image.open(dienstplan_datei)
    text = pytesseract.image_to_string(bild, lang="deu")

    print("\n🔍 OCR-ROH-TEXT:")
    print("-" * 30)
    print(text)
    print("-" * 30 + "\n")

    kalender = Calendar()

    # Regex-Suche für z. B. "15 Di F06"
    matches = re.findall(r"(\d{1,2})\s+\w{2}\s+(F\d{2}|S\d{2}|F01|FO6|F0[1-9])", text)
    for tag_str, raw_code in matches:
        try:
            tag = int(tag_str)
            code = normalize_code(raw_code)
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
                print(f"➕ Eintrag: {event.name} ({start.time()}–{ende.time()})")
        except Exception as e:
            print(f"⚠️ Fehler bei Tag {tag_str}: {e}")

    with open(ics_ziel, "w", encoding="utf-8") as f:
        f.writelines(kalender.serialize_iter())

    print(f"✅ Dienstplan gespeichert als: {ics_ziel}")

if __name__ == "__main__":
    verarbeite_bild()
