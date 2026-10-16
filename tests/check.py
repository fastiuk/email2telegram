"""Verify what the forwarder sent to the Telegram mock: check.py <calls.jsonl> <app.log>"""
import json
import os
import sys

calls = [json.loads(line) for line in open(sys.argv[1], encoding='utf-8')]
log = open(sys.argv[2], encoding='utf-8').read()
sent = [call for call in calls if call['method'].startswith('send')]
texts = [call['fields']['text'] for call in sent if call['method'] == 'sendMessage']
photos = [call['fields'] for call in sent if call['method'] == 'sendPhoto']
documents = [call['fields']['document']['filename'] for call in sent if call['method'] == 'sendDocument']
failures = []


def check(condition: bool, description: str) -> None:
    print('%s %s' % ('ok  ' if condition else 'FAIL', description))
    if not condition:
        failures.append(description)


check(len(texts) == 3, 'three mail summaries sent (got %d)' % len(texts))
check(any('received while offline' in text for text in texts), 'unseen mail received while offline is forwarded')
check(any('Q&A' in text and '100% open' in text for text in texts), 'plain text mail is forwarded')
check(any('&amp; recorded' in text and '🖼' in text for text in texts), 'HTML mail is forwarded with image reference')
check(not any('Newsletter' in text for text in texts), 'mail not matching MAIL_SUBJECT is ignored')
check(not any('Auto' in text for text in texts), 'CUT_FROM_SUBJECT is removed from subjects')
check(len(photos) == 1, 'embedded image is sent as photo (got %d)' % len(photos))
check(documents == ['report.csv'], 'attachment is sent as document (got %s)' % documents)
check(os.environ['TELEGRAM_BOT_TOKEN'] not in log, 'bot token is not logged')
check(os.environ['IMAP_PASSWORD'] not in log, 'IMAP password is not logged')

if failures:
    print('\n--- app log\n' + log)
    sys.exit(1)
