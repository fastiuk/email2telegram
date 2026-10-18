[![GitHub](https://img.shields.io/badge/GitHub-fastiuk%2Femail2telegram-181717?logo=github&logoColor=white)](https://github.com/fastiuk/email2telegram)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-fastiuk%2Femail2telegram-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/fastiuk/email2telegram)
[![Release](https://img.shields.io/github/v/release/fastiuk/email2telegram?logo=github&logoColor=white)](https://github.com/fastiuk/email2telegram/releases)
[![CI](https://img.shields.io/github/actions/workflow/status/fastiuk/email2telegram/docker-image.yml?branch=main&label=CI&logo=githubactions&logoColor=white)](https://github.com/fastiuk/email2telegram/actions/workflows/docker-image.yml)
[![Build](https://img.shields.io/github/actions/workflow/status/fastiuk/email2telegram/docker-publish.yml?branch=main&label=build&logo=docker&logoColor=white)](https://github.com/fastiuk/email2telegram/actions/workflows/docker-publish.yml)
[![Version](https://img.shields.io/docker/v/fastiuk/email2telegram?sort=semver&label=version&logo=docker&logoColor=white)](https://hub.docker.com/r/fastiuk/email2telegram/tags)
[![Docker pulls](https://img.shields.io/docker/pulls/fastiuk/email2telegram?logo=docker&logoColor=white)](https://hub.docker.com/r/fastiuk/email2telegram)
[![Image size](https://img.shields.io/docker/image-size/fastiuk/email2telegram/latest?logo=docker&logoColor=white)](https://hub.docker.com/r/fastiuk/email2telegram/tags)
[![Platform](https://img.shields.io/badge/platform-amd64%20%7C%20arm64%20%7C%20arm%2Fv7-blue?logo=linux&logoColor=white)](#running-the-app)
[![Python](https://img.shields.io/badge/base-Python%20slim-3776AB?logo=python&logoColor=white)](https://hub.docker.com/_/python)
[![Powered by MailToTelegramForwarder](https://img.shields.io/badge/powered%20by-MailToTelegramForwarder-red?logo=telegram&logoColor=white)](https://codeberg.org/Awalon/MailToTelegramForwarder)
[![License](https://img.shields.io/github/license/fastiuk/email2telegram)](LICENSE)

# email2telegram
Email to Telegram forwarder docker service.

Source: [GitHub](https://github.com/fastiuk/email2telegram) ·
Images: [Docker Hub](https://hub.docker.com/r/fastiuk/email2telegram),
[GHCR](https://github.com/fastiuk/email2telegram/pkgs/container/email2telegram)

It watches an IMAP mailbox and forwards new mails (text, HTML, embedded images and attachments)
to a Telegram chat via your bot. Forwarded mails are marked as read in the mailbox.

## Running the app
Images for `amd64`, `arm64` and `arm/v7` are published to
[Docker Hub](https://hub.docker.com/r/fastiuk/email2telegram) and
[GitHub Container Registry](https://github.com/fastiuk/email2telegram/pkgs/container/email2telegram).

```
docker run -d --restart unless-stopped \
    -e IMAP_SERVER=<Server address> \
    -e IMAP_USER=<Username> \
    -e IMAP_PASSWORD=<Password> \
    -e TELEGRAM_BOT_TOKEN=<Token> \
    -e TELEGRAM_CHAT_ID=<Chat ID> \
    -e MAIL_SUBJECT=<Subject to match> \
    -e CUT_FROM_SUBJECT="[Automation]" \
    fastiuk/email2telegram
```

Or with Docker Compose: copy [.env.example](.env.example) to `.env`, fill it in and run
`docker compose up -d` (see [compose.yaml](compose.yaml)).

### Settings

| Variable | Default | Description |
|---|---|---|
| `IMAP_SERVER` | *required* | IMAP server, e.g. `imap.gmail.com` |
| `IMAP_USER` | *required* | IMAP login |
| `IMAP_PASSWORD` | *required* | IMAP password. For Gmail use an [app password](https://support.google.com/accounts/answer/185833) |
| `TELEGRAM_BOT_TOKEN` | *required* | Bot token from [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | *required* | Chat or user ID to forward to, e.g. from [@myidbot](https://t.me/myidbot). Group IDs are negative |
| `MAIL_SUBJECT` | | Forward only mails whose subject contains this text |
| `CUT_FROM_SUBJECT` | | Text to remove from subjects, e.g. a common prefix of automated mails |
| `FORWARD_MAIL_CONTENT` | `True` | `False` sends only embedded images and attachments, with the subject as caption |
| `FORWARD_ATTACHMENT` | `True` | Forward attachments |
| `FORWARD_EMBEDDED_IMAGES` | `True` | Forward images embedded in HTML mails |
| `PREFER_HTML` | `True` | Use the HTML part of a mail rather than plain text |
| `MAX_LENGTH` | `2000` | Max length of forwarded mail text |
| `IGNORE_INLINE_IMAGE` | | Regular expression for inline images to skip, e.g. `(spacer\.gif)` |
| `IMAP_PORT` | `993` | IMAP port (TLS) |
| `IMAP_FOLDER` | `INBOX` | Mailbox folder to watch |
| `IMAP_REFRESH` | `10` | Polling interval in seconds |
| `IMAP_SEARCH` | | Custom IMAP search, replaces the one built from `MAIL_SUBJECT`. `${lastUID}` is replaced with the last processed UID, e.g. `(UID ${lastUID}:* UNSEEN FROM "alerts@example.com")` |
| `READ_OLD_MAILS` | `False` | Kept for compatibility: unseen matching mails are always forwarded, including those received while the container was stopped |

The required settings can also be read from files (Docker secrets) by adding a `_FILE`
suffix, e.g. `IMAP_PASSWORD_FILE=/run/secrets/imap_password`.

## Building docker image
The forwarder is a git submodule, so clone recursively:
```
git clone --recursive https://github.com/fastiuk/email2telegram.git
cd email2telegram
docker build -t email2telegram .
```

## Testing
`tests/e2e.sh` runs the image against a [GreenMail](https://greenmail-mail-test.github.io/greenmail/)
IMAP server and a Telegram Bot API mock, and checks what gets forwarded:
```
docker build -t email2telegram:test .
tests/e2e.sh email2telegram:test
```

## Authors

- **Awalon** - The core service *MailToTelegramForwarder* - 
  [Awalon/MailToTelegramForwarder](https://codeberg.org/Awalon/MailToTelegramForwarder)
  (used via the [fastiuk/MailToTelegramForwarder](https://github.com/fastiuk/MailToTelegramForwarder) fork)

- **Yevhen Fastiuk** - *email2telegram* Docker wrapper - 
  [@fastiuk](https://github.com/fastiuk/email2telegram)

## License

This project and MailToTelegramForwarder are licensed under the *GPLv3 License* - see the 
[LICENSE](LICENSE) file for details.

Some parts (from IMAPBot) are licensed under the *The MIT License (MIT)* - 
see the [LICENSE-MIT.md](https://github.com/awalon/MailToTelegramForwarder/blob/master/LICENSE-MIT.md) file for details.
