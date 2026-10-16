"""Minimal Telegram Bot API mock: answers like the real API and records every call to /tmp/calls.jsonl."""
import email.parser
import email.policy
import json
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CALLS = '/tmp/calls.jsonl'
CHAT = {'id': -100, 'type': 'group', 'title': 'Mock chat'}
message_id = 0


def parse_fields(content_type: str, body: bytes) -> dict:
    if content_type.startswith('multipart/'):
        msg = email.parser.BytesParser(policy=email.policy.default).parsebytes(
            b'Content-Type: ' + content_type.encode() + b'\r\n\r\n' + body)
        fields = {}
        for part in msg.iter_parts():
            name = part.get_param('name', header='content-disposition')
            payload = part.get_payload(decode=True)
            if part.get_filename():
                fields[name] = {'filename': part.get_filename(), 'size': len(payload)}
            else:
                fields[name] = payload.decode()
        return fields
    if 'json' in content_type:
        return json.loads(body or b'{}')
    return {key: values[0] for key, values in urllib.parse.parse_qs(body.decode()).items()}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global message_id
        method = self.path.rsplit('/', 1)[-1]
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        fields = parse_fields(self.headers.get('Content-Type', ''), body)
        with open(CALLS, 'a', encoding='utf-8') as calls:
            calls.write(json.dumps({'method': method, 'fields': fields}, ensure_ascii=False) + '\n')

        message_id += 1
        message = {'message_id': message_id, 'date': int(time.time()), 'chat': CHAT}
        if method == 'getMe':
            result = {'id': 1, 'is_bot': True, 'first_name': 'Mock', 'username': 'mock_bot'}
        elif method == 'getChat':
            result = dict(CHAT, accent_color_id=0, max_reaction_count=11,
                          accepted_gift_types={'unlimited_gifts': False, 'limited_gifts': False,
                                               'unique_gifts': False, 'premium_subscription': False,
                                               'gifts_from_channels': False})
        elif method == 'sendPhoto':
            result = dict(message, photo=[{'file_id': 'photo%d' % message_id, 'file_unique_id': 'p',
                                           'width': 1, 'height': 1}])
        elif method == 'sendDocument':
            result = dict(message, document={'file_id': 'doc%d' % message_id, 'file_unique_id': 'd'})
        else:
            result = message

        out = json.dumps({'ok': True, 'result': result}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *args):
        pass


ThreadingHTTPServer(('0.0.0.0', 8081), Handler).serve_forever()
