FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    wget \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && mkdir -p /usr/share/tesseract-ocr/4.00/tessdata && \
    wget -O /usr/share/tesseract-ocr/4.00/tessdata/deu.traineddata \
    https://github.com/tesseract-ocr/tessdata_best/raw/main/deu.traineddata && \
    mkdir -p /usr/share/tessdata && \
    cp /usr/share/tesseract-ocr/4.00/tessdata/deu.traineddata /usr/share/tessdata/deu.traineddata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV TESSDATA_PREFIX=/usr/share/tessdata

COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY run.py /run.py

CMD ["python3", "/run.py"]
