#!/bin/sh
# End-to-end test: GreenMail (IMAP/SMTP) + Telegram Bot API mock + the email2telegram image.
# Usage: tests/e2e.sh [image]
set -eu

IMAGE=${1:-email2telegram:test}
TESTS=$(cd "$(dirname "$0")" && pwd)
NET=e2t-e2e
OUT=$(mktemp -d)
export TELEGRAM_BOT_TOKEN=123456:E2E-TEST-TOKEN
export IMAP_PASSWORD='s3cr%et "pass"'

cleanup() {
    docker rm -f e2t-mail e2t-tg e2t-app >/dev/null 2>&1 || true
    docker network rm $NET >/dev/null 2>&1 || true
    rm -rf "$OUT"
}
trap cleanup EXIT
cleanup
mkdir -p "$OUT"
docker network create $NET >/dev/null

helper() {
    docker run --rm --network $NET -v "$TESTS:/tests:ro" --entrypoint python3 "$IMAGE" "$@"
}

# number of send* calls the Telegram mock has received
sent() {
    docker exec e2t-tg sh -c 'cat /tmp/calls.jsonl 2>/dev/null' | grep -c '"method": "send' || true
}

wait_for_sent() {
    for _ in $(seq 1 60); do
        [ "$(sent)" -ge "$1" ] && return 0
        sleep 1
    done
    echo "Timeout waiting for $1 Telegram messages, got $(sent)"
    docker logs e2t-app
    exit 1
}

docker run -d --name e2t-mail --network $NET greenmail/standalone:2.1.5 >/dev/null
docker run -d --name e2t-tg --network $NET --network-alias tgmock -v "$TESTS:/tests:ro" \
    --entrypoint python3 "$IMAGE" /tests/tgmock.py >/dev/null

echo "Sending mail before the forwarder starts..."
helper /tests/sendmail.py offline

echo "Starting forwarder..."
docker run -d --name e2t-app --network $NET -v "$TESTS:/tests:ro" \
    -e PYTHONPATH=/tests/pythonpath -e TELEGRAM_API_MOCK=http://tgmock:8081/bot \
    -e IMAP_SERVER=e2t-mail -e IMAP_PORT=3993 -e IMAP_USER=me@example.com -e IMAP_PASSWORD \
    -e TELEGRAM_BOT_TOKEN -e TELEGRAM_CHAT_ID=-100 -e IMAP_REFRESH=1 \
    -e MAIL_SUBJECT=Alarm -e 'CUT_FROM_SUBJECT=[Auto]' \
    "$IMAGE" >/dev/null
wait_for_sent 1

echo "Sending mail while the forwarder runs..."
helper /tests/sendmail.py live
# 2 summaries + 1 photo + 1 attachment
wait_for_sent 5
# give it a few more loops to catch duplicates or unwanted mails
sleep 5

docker stop e2t-app >/dev/null
docker logs e2t-app > "$OUT/app.log" 2>&1
docker exec e2t-tg cat /tmp/calls.jsonl > "$OUT/calls.jsonl"
python3 "$TESTS/check.py" "$OUT/calls.jsonl" "$OUT/app.log"
