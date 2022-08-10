from abc import ABC, abstractmethod
from typing import Dict
from specturm import Spectrum


class QuestionsMapper(ABC):

    """
    sole purpose of this class is to make keys from
    ParsedInterview.question_to_answer be the same as in table where interview codes are stored
    """

    BLOCKS_TO_CODES = {
        1: Spectrum(start=1, end=8),
        2: Spectrum(start=8, end=12),
        3: Spectrum(start=12, end=22),
    }

    @abstractmethod
    def match_questions(self, question_to_answer: Dict[str, str], block: int):
        """matches questions from question_to_answer and table"""

        raise NotImplementedError
