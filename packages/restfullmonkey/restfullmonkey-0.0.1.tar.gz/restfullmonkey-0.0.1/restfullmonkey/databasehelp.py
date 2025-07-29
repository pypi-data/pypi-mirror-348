"""
database helper 
"""
import os
import math
import datetime
from copy import deepcopy


class DatabaseHelpClass:
    """
    database helper class
    :param: logging :
    """
    def __init__(self, logging_):
        self._log     = logging_
        self._checked = False

    def pathFix(self, path_:str)->str:
        """
        path name fix

        :param: str : the record id in str
        :return: str: full path 
        """
        return path_.replace("/", "_")

    def checkDir(self, dir_:str)->bool:
        """
        check dir existance
        :param: str:
        :return: bool:
        """
        if self._checked:
            return False
        if not os.path.exists(
          dir_
        ):
            self._log.debug(
              'Creating database directory'
            )
            os.makedirs(
              dir_
            )
        if not os.path.isdir(
          dir_
        ):
            self._log.critical(
              'Database directory error'
            )
            return True
        self._checked = True
        return False

    def create(
      self,
      id_: int,
      data_: dict[str,any]
    )->dict[str,any]:
        """
        create data structure

        :param: int:
        :param: dict[str, any]:
        :return: dict[str, any]:
        """
        time = math.floor(
          datetime.datetime.timestamp(
            datetime.datetime.now()
          )
        )
        out = {}
        out['data']       = deepcopy(data_)
        out['id']         = deepcopy(id_)
        out['created_at'] = deepcopy(time)
        out['changed_at'] = deepcopy(time)
        return out

    def change(
      self,
      data_: dict[str,any],
      record_: dict[str,any]
    )->dict[str,any]:
        """
        change data structure

        :param: dict[str, any]:
        :param: dict[str, any]:
        :return: dict[str, any]:
        """
        record = {}
        record['id'] = data_['id']
        record['created_at'] = data_['created_at']
        time = math.floor(
          datetime.datetime.timestamp(
            datetime.datetime.now()
          )
        )
        record['data']       = {**data_['data'], **record_}
        record['changed_at'] = time
        return deepcopy(record)

    def extend(
      self,
      data_: dict[str,any],
      record_: dict[str,any]
    )->dict[str,any]:
        """
        extend data structure

        :param: dict[str, any]:
        :param: dict[str, any]:
        :return: dict[str, any]:
        """
        out = deepcopy(record_['data'])
        for i in data_:
            out[i] = data_[i]
        return self.change(out, record_)

    def outdata(
      self,
      data_: dict[str,any]
    )->dict[str,any]:
        """
        output data structure

        :param: dict[str, any]:
        :return: dict[str, any]:
        """
        if data_ == {}:
            return {}
        out       = deepcopy(data_['data'])
        out['id'] = deepcopy(data_['id'])
        return out
