# Dienstplan OCR Add-on für Home Assistant

Dieses Add-on erkennt fotografierte Dienstpläne aus einer Bilddatei (z. B. `dienstplan_04.2025.jpg`)
und erstellt daraus automatisch `.ics`-Kalendereinträge.

## ✅ Funktion

- OCR mit Tesseract (`deu.traineddata`)
- Auswertung typischer Dienstpläne wie: `1 / Mo / F14`
- `.ics` wird im Ordner `/config/www` gespeichert

## 📷 Benutzung

Lege eine Datei in `/config/www/` ab, z. B.:

```
dienstplan_04.2025.jpg
```

Das Add-on erkennt Monat & Jahr und erzeugt automatisch:

```
dienstplan_04.2025.ics
```

## 🔧 Home Assistant Integration

1. Füge in deiner `configuration.yaml` hinzu:

```yaml
calendar:
  - platform: local_calendar
    name: Dienstplan
    file_path: /config/dienstplan.ics
```

2. Kopiere die `.ics` (z. B. per Shell oder Automation) nach:

```
/config/dienstplan.ics
```

3. Starte Home Assistant neu oder lade YAML neu

## 📅 Kalenderanzeige in Lovelace

```yaml
type: calendar
entities:
  - calendar.dienstplan
```

## ⚙️ Automatisierung (Beispiel)

```yaml
trigger:
  - platform: calendar
    event: start
    entity_id: calendar.dienstplan
condition:
  - condition: template
    value_template: "{{ trigger.calendar_event.summary.startswith('Dienst:') }}"
action:
  - service: notify.persistent_notification.create
    data:
      message: "Heute: {{ trigger.calendar_event.summary }}"
```
