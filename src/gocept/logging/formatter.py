import logging
import re


# see logging.Logger.makeRecord()
PREDEFINED_KEYS = set(logging.makeLogRecord({}).__dict__.keys())
PREDEFINED_KEYS.add('message')
PREDEFINED_KEYS.add('asctime')


class KeyValueFormatter(logging.Formatter):

    def format(self, record):
        record.msg += ' ' + self.format_extra(record)
        return super(KeyValueFormatter, self).format(record)

    def format_extra(self, record):
        result = []
        for key, value in record.__dict__.items():
            if key in PREDEFINED_KEYS:
                continue
            result.append('%s=%s' % (key, self.quote(value)))
        return ' '.join(result)

    SIMPLE_WORD = re.compile(r'^[a-zA-Z0-9_.+-]+$')

    def quote(self, value):
        value = str(value)
        if self.SIMPLE_WORD.match(value):
            return value
        return repr(value)


class SyslogKeyValueFormatter(KeyValueFormatter):

    def __init__(self, fmt=None, datefmt=None):
        super(SyslogKeyValueFormatter, self).__init__(
            '%(name)s: %(message)s')
