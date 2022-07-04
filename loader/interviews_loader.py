from abc import ABC, abstractmethod
from typing import Iterable
from interview import RawInterview


class InterviewsLoader(ABC):

    @abstractmethod
    def load(self) -> Iterable[RawInterview]:
        raise NotImplementedError
