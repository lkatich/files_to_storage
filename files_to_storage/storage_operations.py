import collections
import json
import os
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import NamedTuple

from exceptions import HandlerError
from mixins import LogMixin


class UserDataSet(NamedTuple):
    user_id: int
    resource_value: int


class DataSaver(ABC, LogMixin):
    """Interface for data storing: takes dataset per a user (collected from one file) and stores it into some
    storage type: file, DB, or any other storage type"""

    @abstractmethod
    def safe_data(self, data_per_user: UserDataSet, location: str): #DB/table name, filepath
        pass


class FileDataSaver(DataSaver):
    """Class to save data to a local file"""

    def safe_data(self, data_per_user: UserDataSet, location: str):
        """Saves data to file"""
        data = collections.defaultdict(lambda: 0)
        try:
            if self.empty_or_none(location):
                with open(location, "w") as f:
                    data[data_per_user.user_id] += data_per_user.resource_value
                    json.dump(data, f)
            else:
                with open(location, "r+") as f:
                    data = json.load(f)
                    if data_per_user.user_id in data.keys():
                        data[data_per_user.user_id] += data_per_user.resource_value
                    else:
                        data[data_per_user.user_id] = data_per_user.resource_value
                    f.seek(0)
                    json.dump(data, f)
        except JSONDecodeError as ex:
            self._log.debug(f"Json serialization issue happened during data saving to file storage: {ex}")
            raise HandlerError
        except Exception as exc:
            self._log.debug(f"Unexpected issue found as data storing: {exc}")
            raise

    def empty_or_none(self, filepath: str):
        """ Check if file exists or is empty by confirming if its size is 0 bytes"""
        return not os.path.exists(filepath) or os.stat(filepath).st_size == 0


