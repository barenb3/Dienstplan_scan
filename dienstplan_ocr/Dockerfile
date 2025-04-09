FROM python:3.11-slim

# Tesseract installieren
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Sprachdatei manuell herunterladen
RUN mkdir -p /usr/share/tessdata && \
    wget -O /usr/share/tessdata/deu.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/deu.traineddata

# OCR-Sprachdaten-Pfad setzen
ENV TESSDATA_PREFIX=/usr/share/

# Python-Abhängigkeiten
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Code
COPY run.py /run.py

CMD ["python", "/run.py"]
