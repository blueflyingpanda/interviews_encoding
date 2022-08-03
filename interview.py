from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class RawInterview:
    code: str
    content: Optional[str]


@dataclass
class ParsedInterview(RawInterview):
    question_to_answer: Dict[str, str]
    code_to_answer: Dict[str, str]
    duration: str = ''
    date: str = ''
    interviewer_name: str = ''
    respondent_name: str = ''
    respondent_expertise: str = ''
