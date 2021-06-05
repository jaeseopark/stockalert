import logging


class LambdaLogFormatter(logging.Formatter):
    def format(self, record):
        result = super().format(record)
        return result.replace('\n', '\r')


def configure():
    root_logger = logging.root

    if len(root_logger.handlers) > 0:
        root_logger.setLevel(logging.INFO)
        for handler in root_logger.handlers:
            fmt = LambdaLogFormatter(handler.formatter._fmt)
            handler.setFormatter(fmt)
