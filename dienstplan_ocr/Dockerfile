FROM python:3.11-alpine

# Systempakete installieren: Tesseract + deutsche Sprache
RUN apk add --no-cache tesseract-ocr tesseract-ocr-deu

# Python-Abhängigkeiten
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Code kopieren
COPY run.py /run.py

CMD ["python", "/run.py"]
