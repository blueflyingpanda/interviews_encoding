from abc import ABC, abstractmethod
from interview import RawInterview, ParsedInterview


class InterviewParser(ABC):

    INTERVIEW_STARTS = {'скажите', 'сказать'}
    INTERVIEWER_LABEL = 'И'
    RESPONDENT_LABEL = 'Р'
    HEADER_FIELDS = {
        'date': 'Дата проведения интервью',
        'respondent_name': 'Фамилия, имя эксперта',  # no colon
        'interviewer_name': 'Интервьюер',
        'respondent_expertise': 'Должность',
        'duration': 'Длительность интервью по файлу записи'
    }

    @abstractmethod
    def parse(self, interview: RawInterview) -> ParsedInterview:
        raise NotImplementedError
