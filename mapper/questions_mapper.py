from abc import ABC, abstractmethod
from typing import Dict


class QuestionsMapper(ABC):

    """
    sole purpose of this class is to make keys from
    ParsedInterview.question_to_answer be the same as in table where interview codes are stored
    """

    @abstractmethod
    def match_questions(self, question_to_answer: Dict[str, str]):
        """matches questions from question_to_answer and table"""

        raise NotImplementedError
