# Dienstplan OCR Add-on für Home Assistant 📅🧠

Dieses Add-on erkennt fotografierte Dienstpläne im JPG-Format und erstellt automatisch `.ics`-Kalendereinträge, die sich in Home Assistant einbinden lassen.

## ✅ Funktionen

- Automatische Texterkennung (OCR) mit Tesseract
- Unterstützt Schichtformate wie `F06`, `F14`, `S04`, usw.
- Generiert `.ics`-Kalenderdateien im Ordner `/config/www`
- Kompatibel mit lokalem Kalender oder externem Import

## 📷 Datei-Format

Lege ein Bild mit dem Namen `dienstplan_MM.JJJJ.jpg` in den Ordner `/config/www`, z. B.:

```
/config/www/dienstplan_04.2025.jpg
```

## ⚙️ Installation

1. Dieses Repository zu GitHub hochladen
2. In Home Assistant hinzufügen unter:  
   **Einstellungen → Add-ons → Repositories → `https://github.com/deinname/dienstplan_ocr`**
3. Add-on installieren & starten

## 📌 Voraussetzung

- Home Assistant 2023.0.0 oder neuer
- Aktivierte lokale Kalender-Funktion (optional für Anzeige)

## 🧠 Hinweis

Das Add-on analysiert nur Bilder mit einem klar erkennbaren Datum + Schichtcode pro Zeile.
