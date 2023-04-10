# syntax=docker/dockerfile:1
   
FROM ubuntu:22.04

WORKDIR /app

RUN apt update
RUN apt install -y \
    python3-python-telegram-bot \
    python3-imaplib2 \
    j2cli

COPY MailToTelegramForwarder .
COPY mailToTelegramForwarder.conf.j2 .
COPY start.sh .

RUN chmod +x mailToTelegramForwarder.py

ENV IMAP_SERVER "server"
ENV IMAP_USER "user"
ENV IMAP_PASSWORD "pass"
ENV TELEGRAM_BOT_TOKEN ""
ENV TELEGRAM_CHAT_ID ""

RUN j2 mailToTelegramForwarder.conf.j2 > mailToTelegramForwarder.conf
RUN cat mailToTelegramForwarder.conf


#CMD ./start.sh
ENTRYPOINT ./start.sh
#EXPOSE 3000
