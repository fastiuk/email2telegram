[![Project: email2telegram](https://img.shields.io/badge/Project-email2telegram-red.svg?style=flat-square)](https://github.com/fastiuk/email2telegram)
[![Powered by: MailToTelegramForwarder](https://img.shields.io/badge/Powered%20by-MailToTelegramForwarder-red.svg?style=flat-square)](https://github.com/awalon/MailToTelegramForwarder)

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/fastiuk/email2telegram)
![GitHub CI](https://img.shields.io/github/actions/workflow/status/fastiuk/email2telegram/docker-image.yml?branch=main&label=CI&style=flat-square&logo=github)
[![GitHub issues](https://img.shields.io/github/issues/fastiuk/email2telegram?style=flat-square)](https://github.com/fastiuk/email2telegram/issues)
![Protocol: IMAP](https://img.shields.io/badge/Protocol-IMAP-blue?style=flat-square&logo=Gmail)
![API: Telegram Bot](https://img.shields.io/badge/API-Telegram_Bot-informational?style=flat-square&logo=telegram)
[![License: GPL + MIT](https://img.shields.io/badge/license-GPL+MIT-informational?style=flat-square)](README.md#license)
[![GitHub forks](https://img.shields.io/github/forks/fastiuk/email2telegram?style=flat-square)](https://github.com/fastiuk/email2telegram/network) 
[![GitHub stars](https://img.shields.io/github/stars/fastiuk/email2telegram?style=flat-square)](https://github.com/fastiuk/email2telegram/stargazers)

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

## Authors

- **Awalon** - The core service *MailToTelegramForwarder* - 
  [@awalon](https://github.com/awalon/MailToTelegramForwarder)

- **Yevhen Fastiuk** - *email2telegram* Docker wrapper - 
  [@fastiuk](https://github.com/fastiuk/email2telegram)

## License

This project and MailToTelegramForwarder are licensed under the *GPLv3 License* - see the 
[LICENSE.md](LICENSE.md) file for details.

Some parts (from IMAPBot) are licensed under the *The MIT License (MIT)* - 
see the [LICENSE-MIT.md](LICENSE-MIT.md) file for details.
