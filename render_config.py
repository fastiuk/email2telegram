#!/usr/bin/env python3
"""Render the MailToTelegramForwarder config from environment variables."""
import os
import sys

from jinja2 import Environment, FileSystemLoader

REQUIRED = ('IMAP_SERVER', 'IMAP_USER', 'IMAP_PASSWORD', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID')


def load_env() -> dict[str, str]:
    env = dict(os.environ)
    # Docker secrets: IMAP_PASSWORD_FILE=/run/secrets/imap_password sets IMAP_PASSWORD
    for key in REQUIRED:
        path = env.get(key + '_FILE')
        if path and not env.get(key):
            with open(path, encoding='utf-8') as secret:
                env[key] = secret.read().strip()
    return env


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit('Usage: render_config.py <template>')

    env = load_env()
    missing = [key for key in REQUIRED if not env.get(key)]
    if missing:
        sys.exit('Missing required environment variables: ' + ', '.join(missing))

    template_dir, template_name = os.path.split(os.path.abspath(sys.argv[1]))
    jinja = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True,
                        lstrip_blocks=True, keep_trailing_newline=True)
    sys.stdout.write(jinja.get_template(template_name).render(env))


if __name__ == '__main__':
    main()
