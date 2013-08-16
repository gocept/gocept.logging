import logging


class StaticDefaults(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        if 'extra' in kwargs:
            extra = self.extra.copy()
            extra.update(kwargs['extra'])
            kwargs['extra'] = extra
        else:
            kwargs['extra'] = self.extra
        return msg, kwargs
