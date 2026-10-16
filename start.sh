#!/bin/sh
set -eu

CONFIG=/tmp/mailToTelegramForwarder.conf

# the rendered config holds credentials: keep it private and never print it
umask 077
python3 /app/render_config.py /app/mailToTelegramForwarder.conf.j2 > "$CONFIG"

exec python3 /app/mailToTelegramForwarder.py --config "$CONFIG"
