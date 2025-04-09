FROM python:3.11-slim

# Systempakete und deutsche Sprachdaten installieren
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-deu \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten installieren
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Tesseract Sprachdaten-Umgebungsvariable setzen (optional, meist nicht nötig)
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# Code kopieren
COPY run.py /run.py

CMD ["python", "/run.py"]
