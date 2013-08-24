from gocept.logging.adapter import StaticDefaults
import gocept.logging
import logging
import unittest


class StaticDefaultsTest(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('test')
        self.handler = gocept.logging.TestingHandler()
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(self.handler)

    def tearDown(self):
        self.log.handlers[:] = []

    def test_adds_extra_values(self):
        log = StaticDefaults(self.log, {'qux': 'baz'})
        log.warning('')
        self.assertEqual(
            {'qux': 'baz'}, self.handler.messages[0].extra)

    def test_adds_extra_values_to_the_one_from_logger(self):
        log = StaticDefaults(self.log, {'qux': 'baz'})
        log.warning('', extra={'foo': 'bar'})
        self.assertEqual(
            {'foo': 'bar', 'qux': 'baz'}, self.handler.messages[0].extra)

    def test_logger_overrides_values(self):
        log = StaticDefaults(self.log, {'foo': 'bar'})
        log.warning('', extra={'foo': 'over'})
        self.assertEqual({'foo': 'over'}, self.handler.messages[0].extra)
