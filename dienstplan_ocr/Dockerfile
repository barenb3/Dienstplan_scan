ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache tesseract-ocr py3-pillow py3-pip py3-setuptools py3-virtualenv py3-wheel

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY run.py /run.py

CMD ["python3", "/run.py"]
