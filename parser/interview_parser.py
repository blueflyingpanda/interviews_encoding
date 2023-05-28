from abc import ABC, abstractmethod

from features.keywords_extractor import KeywordsExtractor
from features.sentiment_analyzer import SentimentAnalyzer
from interview import RawInterview, ParsedInterview


class BaseInterviewParser(ABC):

    SENTIMENT_ANALYSIS_LABEL = 'SA'
    KEYWORDS_LABEL = 'KW'
    additional_features = {
        SENTIMENT_ANALYSIS_LABEL: SentimentAnalyzer.analyze_sentiment,
        KEYWORDS_LABEL: KeywordsExtractor.extract_keywords
    }

    INTERVIEWER_LABEL = 'И'
    RESPONDENT_LABEL = 'Р'

    HEADER_FIELDS = {
         'дата': 'date',
         'эксперт': 'respondent_name',
         'интервьюер': 'interviewer_name',
         'должность': 'respondent_expertise',
         'длительность': 'duration'
    }

    @abstractmethod
    def parse(self, interview: RawInterview) -> ParsedInterview:
        raise NotImplementedError
