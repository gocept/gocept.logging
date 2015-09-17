import argparse
import logging


class ArgumentParser(argparse.ArgumentParser):

    LOG_FORMAT = logging.BASIC_FORMAT

    def __init__(self, *args, **kw):
        super(ArgumentParser, self).__init__(*args, **kw)
        self.add_argument('-q', '--quiet', action='count', default=0,
                          help='Log less info. (may be used up to twice.)')
        self.add_argument('-v', '--verbose', action='count', default=0,
                          help='Log more info. (may be used up to twice.)')

    def parse_args(self, *args, **kw):
        options = super(ArgumentParser, self).parse_args(*args, **kw)

        verbosity = options.verbose - options.quiet
        if verbosity <= -2:
            log_level = 'CRITICAL'
        elif verbosity == -1:
            log_level = 'ERROR'
        elif verbosity == 0:
            log_level = 'WARNING'
        elif verbosity == 1:
            log_level = 'INFO'
        else:
            log_level = 'DEBUG'

        self.setup_logging(log_level)
        options.log_level = log_level
        return options

    def setup_logging(self, level):
        logging.basicConfig(level=level, format=self.LOG_FORMAT)
