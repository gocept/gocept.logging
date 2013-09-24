try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import gocept.logging
import logging
import unittest


class KeyValueFormatter(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger('test')
        self._output = StringIO()
        handler = logging.StreamHandler(self._output)
        handler.setFormatter(gocept.logging.SyslogKeyValueFormatter())
        self.log.addHandler(handler)

    def tearDown(self):
        self.log.handlers[:] = []

    @property
    def output(self):
        return self._output.getvalue()

    def test_appends_key_value_pairs_after_message(self):
        self.log.warning('Hello, world!', extra={'foo': 'bar'})
        self.assertIn("test: Hello, world! foo=bar\n", self.output)

    def test_empty_value_is_quoted(self):
        self.log.warning('', extra={'foo': ''})
        self.assertIn("foo=''", self.output)

    def test_simple_strings_are_not_quoted(self):
        self.log.warning('', extra={'foo': 'bar'})
        self.assertIn('foo=bar', self.output)

    def test_floats_are_not_quoted(self):
        self.log.warning('', extra={'foo': 1.5e-5})
        self.assertIn('foo=1.5e-05', self.output)

    def test_spaces_are_quoted_with_single(self):
        self.log.warning('', extra={'foo': 'bar baz'})
        self.assertIn("foo='bar baz'", self.output)

    def test_single_quotes_are_quoted_with_double(self):
        self.log.warning('', extra={'foo': "bar'baz"})
        self.assertIn('foo="bar\'baz"', self.output)

    def test_objects_in_extra_are_serialized_to_string(self):
        self.log.warning('', extra={'foo': object()})
        self.assertRegexpMatches(self.output, "foo='<object object at 0x.*>'")

    def test_objects_in_message_are_serialized_to_string(self):
        self.log.warning(object())
        self.assertRegexpMatches(self.output, "<object object at 0x.*>")
