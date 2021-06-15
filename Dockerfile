FROM python:3-slim

RUN mkdir -p /src
COPY setup.py /src
COPY me.py /src

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir /src/

RUN rm -rf /src

CMD ["mifi-exporter", "--help"]
