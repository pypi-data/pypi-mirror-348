import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__version__ = "0.0.0"  # will be set at runtime
logger.info(f"MouseTools version: {__version__}")
