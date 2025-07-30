import logging


def setup_logging(level=logging.DEBUG):
    formatter = logging.Formatter(
        "%(levelname)s %(name)s: %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)