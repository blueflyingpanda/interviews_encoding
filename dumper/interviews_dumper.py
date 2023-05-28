from abc import ABC, abstractmethod
from interview import ParsedInterview
from typing import List


class BaseInterviewsDumper(ABC):

    @abstractmethod
    def dump(self, interviews: List[ParsedInterview]) -> None:
        raise NotImplementedError
