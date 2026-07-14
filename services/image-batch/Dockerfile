FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

COPY services/image-batch/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/acps_shared/ ./acps_shared/
COPY services/image-batch/app/ ./app/

RUN useradd --system --no-create-home --uid 1001 appuser
USER appuser

ENTRYPOINT ["python", "-m", "app"]
