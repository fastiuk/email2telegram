"""Send test mails to the GreenMail SMTP server: sendmail.py offline|live"""
import smtplib
import sys
import time
from email.message import EmailMessage

SMTP = ('e2t-mail', 3025)
TO = 'me@example.com'
# 1x1 transparent PNG
PNG = bytes.fromhex('89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489'
                    '0000000d49444154789c6360f8cfc0f01f0005000201e5274d1e0000000049454e44ae426082')


def plain(subject: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg['From'] = 'Alarm system <alarm@example.com>'
    msg['To'] = TO
    msg['Subject'] = subject
    msg.set_content(body)
    return msg


def html_with_image(subject: str) -> EmailMessage:
    msg = EmailMessage()
    msg['From'] = 'Camera <cam@example.com>'
    msg['To'] = TO
    msg['Subject'] = subject
    msg.set_content('plain fallback')
    msg.add_alternative('<html><body><p>Motion <b>detected</b> &amp; recorded</p>'
                        '<img src="cid:snap1" alt="Snapshot"></body></html>', subtype='html')
    msg.get_payload()[1].add_related(PNG, 'image', 'png', cid='<snap1>', filename='snap.png',
                                     disposition='inline')
    msg.add_attachment(b'col1,col2\n1,2\n', maintype='text', subtype='csv', filename='report.csv')
    return msg


MAILS = {
    'offline': [plain('[Auto] Alarm: received while offline', 'Old unseen mail')],
    'live': [plain('[Auto] Alarm: Q&A <door> 100% open', 'Front door is *open*_now [check]'),
             html_with_image('[Auto] Alarm with image'),
             plain('Newsletter', 'should NOT be forwarded')],
}


def connect() -> smtplib.SMTP:
    for _ in range(60):
        try:
            return smtplib.SMTP(*SMTP, timeout=5)
        except OSError:
            time.sleep(1)
    sys.exit('SMTP server %s:%d is not reachable' % SMTP)


with connect() as smtp:
    for mail in MAILS[sys.argv[1]]:
        smtp.send_message(mail)
