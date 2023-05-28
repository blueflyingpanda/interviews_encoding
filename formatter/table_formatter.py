from abc import ABC, abstractmethod


class BaseTableFormatter(ABC):

    width = 42

    @classmethod
    @abstractmethod
    def format(cls, table_path, format_delimiter):
        raise NotImplementedError
