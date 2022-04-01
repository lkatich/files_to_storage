import datetime
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, Future
from logging.config import dictConfig
from pathlib import Path
from threading import RLock

import yaml

from exceptions import HandlerError
from mixins import LogMixin
from reader import FileReader
from storage_operations import UserDataSet, FileDataSaver

WD = Path(__file__).parent

# Set up logging
with open(WD/'conf'/'log_config.yml') as file:
    dictConfig(yaml.safe_load(file))

with open(WD/'conf'/'config.yml') as file:
    cfg = yaml.safe_load(file)


class DataHandler(LogMixin):
    def __init__(self):
        super().__init__()
        self.proc_files = {}
        self.files_location = f"{WD.parent}/{cfg['FILES_FOLDER_PATH']}"
        self.proc_files_location = f"{WD.parent}/{cfg['PROCESSED_FILES']}"
        self.fds = FileDataSaver()
        self.reader = FileReader(cfg['CHUNK_SIZE'], working_dir=self.files_location)
        self._executor = ThreadPoolExecutor(max_workers=cfg['MAX_WORKERS'])
        self.lock = RLock()
        self.files_to_process = []

    def run(self):
        """Main function to start the loop for checking new files arrived"""
        if not os.path.exists(self.proc_files_location):
            open(self.proc_files_location, 'a').close()
        while True:
            self._log.debug("Searching for the new files...")
            self.proc_files = self.reader.read_yml_file(self.proc_files_location)
            all_files = os.listdir(self.files_location)
            for f in all_files:
                if f not in self.proc_files.keys() and f not in self.files_to_process:
                    self._log.debug(f"Found new file: {f}")
                    self.files_to_process.append(f)

            self._log.debug(f"Files to process: {self.files_to_process}")

            for f in self.files_to_process:
                self._make_task(self.handle_new_file, filepath = f)
                self.files_to_process.remove(f)

            time.sleep(cfg['WATCH_PERIOD'])

    def handle_new_file(self, filepath: str):
        """Takes filepath and processes the data from the file - reads and stores"""
        data = self.reader.read_text_file(filepath)
        for k, v in data.items():
            user_data = UserDataSet(k, v)
            with self.lock:
                self.fds.safe_data(user_data, f"{WD.parent}/{cfg['STORAGE_FILE']}")

            self.proc_files[filepath] = {'done': True, 'time': datetime.datetime.now()}
            with self.lock:
                with open(self.proc_files_location, "w") as f:
                    f.write(yaml.dump(self.proc_files, default_flow_style=False))

    def _make_task(self, func, **kwargs) -> Future:
        """Function to handle the requests in threads"""
        future = self._executor.submit(func, **kwargs)

        def log_exceptions(done_future: Future):
            try:
                done_future.result()

            # For some kind of possible predictable errors
            except HandlerError as ex:
                self._log.error(f'EXCEPTION in task thread: {ex}')
                raise

            # For WTFs
            except Exception as ex:
                self._log.critical(f'FAIL: {ex}\n{traceback.format_exc()}')
                raise

        future.add_done_callback(log_exceptions)
        return future


if __name__ == '__main__':
    t = DataHandler()
    t.run()












