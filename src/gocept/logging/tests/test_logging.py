from StringIO import StringIO
import gocept.logging
import logging
import unittest


class KeyValueFormatter(unittest.TestCase):

    def test_appends_key_value_pairs_after_message(self):
        output = StringIO()
        log = logging.getLogger('test')
        handler = logging.StreamHandler(output)
        handler.setFormatter(gocept.logging.SyslogKeyValueFormatter())
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)

        log.debug('Hello, world!', extra={'foo': 'bar'})
        self.assertEqual("test: Hello, world! foo='bar'\n", output.getvalue())
