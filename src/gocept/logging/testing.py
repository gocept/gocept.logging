import collections
import gocept.logging.formatter
import logging


LogMessage = collections.namedtuple(
    'LogMessage', ['name', 'levelname', 'message', 'extra'])


class TestingHandler(logging.Handler):

    def __init__(self, *args, **kw):
        super(TestingHandler, self).__init__(*args, **kw)
        self.messages = []

    def emit(self, record):
        extra = {}
        for key, value in record.__dict__.items():
            if key in gocept.logging.formatter.PREDEFINED_KEYS:
                continue
            extra[key] = value
        self.messages.append(
            LogMessage(record.name, record.levelname, record.msg, extra))
