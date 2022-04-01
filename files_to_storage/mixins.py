import json
import logging
from typing import Dict


class LogMixin:

    def __init__(self, subname: str = None):
        name = self.__class__.__name__ + (f'({subname})' if subname else '')
        self._log = logging.getLogger(name)

    def log_json(self, data: Dict, description: str = ''):
        self._log.debug(f'{description}\n{json.dumps(data, indent=4)}')