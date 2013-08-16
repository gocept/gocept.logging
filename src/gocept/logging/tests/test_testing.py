from gocept.logging.testing import LogMessage
import gocept.logging
import logging
import unittest


class TestingHandlerTest(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('test')

    def tearDown(self):
        self.log.handlers[:] = []

    def test_inspect_extra_values(self):
        handler = gocept.logging.TestingHandler()
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(handler)

        self.log.warning('Hello, world!', extra={'foo': 'bar'})
        self.assertEqual(
            [LogMessage('test', 'WARNING', 'Hello, world!', {'foo': 'bar'})],
            handler.messages)
