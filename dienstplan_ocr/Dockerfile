FROM python:3.11-slim

# Tesseract + Sprachdaten installieren
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-deu \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Umgebungsvariable setzen für Tesseract
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/

# Python-Abhängigkeiten installieren
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Code kopieren
COPY run.py /run.py

CMD ["python", "/run.py"]
