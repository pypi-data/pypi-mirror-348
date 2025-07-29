"""Logging setup"""

import logging

DEFAULT_FORMAT = "[%(asctime)s][%(levelname)-7.7s] | %(message)s [%(filename)s:%(funcName)s:%(lineno)d]"
LOGGER = logging.getLogger(__name__)
