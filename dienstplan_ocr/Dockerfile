FROM python:3.11-alpine

# Installiere Systemabhängigkeit für pytesseract
RUN apk add --no-cache tesseract-ocr

# Kopiere Code und Requirements
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY run.py /run.py

CMD ["python", "/run.py"]
