import collections
import re
import time
from typing import DefaultDict
from mixins import LogMixin
import psutil
import yaml


class FileReader(LogMixin):
    def __init__(self, chunk_size: int, working_dir: str):
        super().__init__()
        self.WD = working_dir

    def read_yml_file(self, filepath: str):
        with open(filepath) as f:
            try:
                from_file = yaml.safe_load(f)
                return from_file if from_file is not None else {}
            except yaml.YAMLError as exc:
                self._log.critical(f"File can't be read due to yml issue: {exc}")
                raise

    def read_text_file(self, filepath: str) -> DefaultDict:
        if not self.is_in_use(filepath):
            # read isn't a blocking operation however we need to avoid the case when the file is too big and though
            # it's been already created in the directory - hasn't been fully filled with data -> make 1 s wait and retry
            processed_data = collections.defaultdict(lambda: 0)
            pattern = r"(\d*)\s(\d*)"
            with open(f"{self.WD}/{filepath}", "r") as f:
                for line in (line for line in f):
                    if match := re.search(pattern, line):
                        id = match.group(1)
                        resource = match.group(2)
                        processed_data[id] += int(resource)
                    else:
                        if len(line) > 0:
                            self._log.debug(f"Found a line which doesn't match. File: {filepath}. Line: {line}")
            return processed_data
        else:
            time.sleep(1)
            self.process_text(filepath)

    @staticmethod
    def is_in_use(f):
        for proc in psutil.process_iter():
            try:
                for item in proc.open_files():
                    if f == item.path:
                        return True
            except Exception:
                pass
        return False
