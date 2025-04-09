FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    wget \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata && \
    wget -O /usr/share/tesseract-ocr/4.00/tessdata/deu.traineddata \
    https://github.com/tesseract-ocr/tessdata/raw/main/deu.traineddata

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY run.py /run.py

CMD ["python", "/run.py"]
