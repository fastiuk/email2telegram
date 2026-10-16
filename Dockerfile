# syntax=docker/dockerfile:1

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY MailToTelegramForwarder/mailToTelegramForwarder.py .
COPY mailToTelegramForwarder.conf.j2 render_config.py start.sh ./
RUN chmod +x start.sh mailToTelegramForwarder.py

RUN useradd --system --no-create-home --uid 10001 app
USER app

# The forwarder stops cleanly on Ctrl+C (KeyboardInterrupt)
STOPSIGNAL SIGINT

ENTRYPOINT ["/app/start.sh"]
