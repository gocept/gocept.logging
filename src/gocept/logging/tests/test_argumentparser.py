import unittest
import mock


class ArgumentParserTests(unittest.TestCase):

    def test_adds_quiet_and_verbose_arguments_per_default(self):
        from gocept.logging import ArgumentParser
        parser = ArgumentParser()
        destinations = [a.dest for a in parser._actions]
        self.assertIn('quiet', destinations)
        self.assertIn('verbose', destinations)

    def test_ERROR_if_quiet(self):
        from gocept.logging import ArgumentParser
        parser = ArgumentParser()
        with mock.patch('gocept.logging.argumentparser.ArgumentParser.'
                        'setup_logging') as setup_logging:
            options = parser.parse_args(['-q'])
            self.assertEqual(options.quiet, 1)
            self.assertEqual(options.verbose, 0)
            setup_logging.assert_called_with('ERROR')

    def test_CRITICAL_if_more_quiet(self):
        from gocept.logging import ArgumentParser
        parser = ArgumentParser()
        with mock.patch('gocept.logging.argumentparser.ArgumentParser.'
                        'setup_logging') as setup_logging:
            options = parser.parse_args(['-qq'])
            self.assertEqual(options.quiet, 2)
            self.assertEqual(options.verbose, 0)
            setup_logging.assert_called_with('CRITICAL')

    def test_WARNING_by_default(self):
        from gocept.logging import ArgumentParser
        parser = ArgumentParser()
        with mock.patch('gocept.logging.argumentparser.ArgumentParser.'
                        'setup_logging') as setup_logging:
            options = parser.parse_args([])
            self.assertEqual(options.quiet, 0)
            self.assertEqual(options.verbose, 0)
            setup_logging.assert_called_with('WARNING')

    def test_INFO_if_verbose(self):
        from gocept.logging import ArgumentParser
        parser = ArgumentParser()
        with mock.patch('gocept.logging.argumentparser.ArgumentParser.'
                        'setup_logging') as setup_logging:
            options = parser.parse_args(['-v'])
            self.assertEqual(options.quiet, 0)
            self.assertEqual(options.verbose, 1)
            setup_logging.assert_called_with('INFO')

    def test_DEBUG_if_more_verbose(self):
        from gocept.logging import ArgumentParser
        parser = ArgumentParser()
        with mock.patch('gocept.logging.argumentparser.ArgumentParser.'
                        'setup_logging') as setup_logging:
            options = parser.parse_args(['-vv'])
            self.assertEqual(options.quiet, 0)
            self.assertEqual(options.verbose, 2)
            setup_logging.assert_called_with('DEBUG')
