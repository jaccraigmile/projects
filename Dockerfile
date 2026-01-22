FROM python:3.11-slim

WORKDIR /service

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY clamav_service.py .
COPY service_manifest.yml .

ENV SERVICE_PATH=/service

CMD ["python", "-m", "assemblyline_service.run"]
