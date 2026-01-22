FROM ghcr.io/cybercentrecanada/assemblyline-service-base:latest

WORKDIR /service

COPY clamav_service.py .
COPY service_manifest.yml .

ENV SERVICE_PATH=/service
