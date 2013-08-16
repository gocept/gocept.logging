from gocept.logging.testing import LogMessage
from StringIO import StringIO
import gocept.logging
import logging
import unittest


class KeyValueFormatter(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('test')

    def tearDown(self):
        self.log.handlers[:] = []

    def test_appends_key_value_pairs_after_message(self):
        output = StringIO()
        handler = logging.StreamHandler(output)
        handler.setFormatter(gocept.logging.SyslogKeyValueFormatter())
        self.log.addHandler(handler)

        self.log.warning('Hello, world!', extra={'foo': 'bar'})
        self.assertEqual("test: Hello, world! foo='bar'\n", output.getvalue())

    def test_inspect_extra_values(self):
        handler = gocept.logging.TestingHandler()
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(handler)

        self.log.warning('Hello, world!', extra={'foo': 'bar'})
        self.assertEqual(
            [LogMessage('test', 'WARNING', 'Hello, world!', {'foo': 'bar'})],
            handler.messages)
