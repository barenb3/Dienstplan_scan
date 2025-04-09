FROM python:3.11-alpine

# Installiere Tesseract + deutsche Sprachdaten
RUN apk add --no-cache tesseract-ocr tesseract-ocr-deu

# Tesseract auf Verzeichnis für Sprachdaten hinweisen
ENV TESSDATA_PREFIX=/usr/share/tessdata

# Python-Abhängigkeiten installieren
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Script kopieren
COPY run.py /run.py

CMD ["python", "/run.py"]
