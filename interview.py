from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class RawInterview:
    code: str
    content: str


@dataclass
class ParsedInterview(RawInterview):
    code_to_answer: Optional[Dict[int, str]] = None
    duration: str = ''
    date: str = ''
    interviewer_name: str = ''
    respondent_name: str = ''
    respondent_expertise: str = ''
