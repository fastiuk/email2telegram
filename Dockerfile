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
ENV MAIL_SUBJECT ""
ENV READ_OLD_MAILS "False"
ENV CUT_FROM_SUBJECT ""
ENV FORWARD_MAIL_CONTENT "True"

#CMD ./start.sh
ENTRYPOINT ./start.sh
#EXPOSE 3000
