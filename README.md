# email2telegram
Email to Telegram forwarder docker service

## Building docker image
Run the next command:
```
cd email2telegram
docker build -t email2telegram .
```

## Running the app
Run this command with proper data set to variables:
```
docker run \
    -e IMAP_USER=<Username> \
    -e IMAP_PASSWORD=<Password> \
    -e IMAP_SERVER=<Server address> \
    -e TELEGRAM_BOT_TOKEN=<Token> \
    -e TELEGRAM_CHAT_ID=<Chat ID> \
    -e READ_OLD_MAILS=False \
    -e MAIL_SUBJECT=<Subject to match> \
    email2telegram
```
