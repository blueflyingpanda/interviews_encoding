from abc import ABC, abstractmethod
from typing import Iterable
from interview import RawInterview


class BaseInterviewsLoader(ABC):

    @abstractmethod
    def load(self) -> Iterable[RawInterview]:
        raise NotImplementedError
