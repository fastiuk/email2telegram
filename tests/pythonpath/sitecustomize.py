"""Point python-telegram-bot at the Bot API mock. Loaded through PYTHONPATH by tests/e2e.sh only."""
import os

import telegram

_bot_init = telegram.Bot.__init__


def _bot_init_with_mock(self, *args, **kwargs):
    kwargs.setdefault('base_url', os.environ['TELEGRAM_API_MOCK'])
    _bot_init(self, *args, **kwargs)


telegram.Bot.__init__ = _bot_init_with_mock
