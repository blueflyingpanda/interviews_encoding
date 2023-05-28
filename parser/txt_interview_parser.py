from answer import Answer
from exceptions import ParserException
from parser.interview_parser import BaseInterviewParser
from interview import RawInterview, ParsedInterview
from typing import Dict, List, Set
import re


class TxtInterviewParser(BaseInterviewParser):

    """
    parses interviews in text format (.txt)
    """

    def __init__(self, block_delimiter):
        self.block_delimiter = block_delimiter

    def parse(self, raw_interview: RawInterview) -> ParsedInterview:
        parsed_interview = ParsedInterview(
            code=raw_interview.code,
            content=raw_interview.content.replace(' ', '')  # ' ' - Non-breaking space
        )
        blocks = parsed_interview.content.split(sep=self.block_delimiter)
        if not blocks:
            raise ParserException('No content of interview found. Probably wrong formatting.')
        header = blocks.pop(0)
        self._add_meta_from(header, parsed_interview)
        parsed_interview.code_to_answer = self._parse_codes_to_answers(blocks)

        return parsed_interview

    def _add_meta_from(self, header: str, parsed_interview: ParsedInterview):
        # remove brackets
        header = re.sub(r'\((.+?)\)', '', header)

        # tokens are fields and values. Order: first field, next corresponding value
        tokens = [token.strip() for token in header.split('\n') if token.strip()]
        fields = [tokens[i].lower() for i in range(len(tokens)) if not i % 2]
        values = [tokens[i] for i in range(len(tokens)) if i % 2]

        if len(fields) != len(values) or set(fields) != set(self.HEADER_FIELDS.keys()):
            raise ParserException('Failed to parse metadata. Wrong header formatting.')

        # fill in parsed_interview
        for field, value in zip(fields, values):
            setattr(parsed_interview, self.HEADER_FIELDS[field], value)

    def _parse_codes_to_answers(self, blocks: List[str]) -> Dict[int, Answer]:
        codes_to_answers = {}
        for block in blocks:
            code_info, block_text = block.split(sep='\n', maxsplit=1)
            code_info = code_info.split()
            code = int(code_info.pop(0))
            enabled_features = {info for info in code_info if info in self.additional_features}
            answers = [
                answer[len(self.RESPONDENT_LABEL) + 1:].strip()  # + 1 to remove colon
                for answer in block_text.split(sep='\n')
                if answer.strip().startswith(self.RESPONDENT_LABEL)
            ]
            answer = self._generate_answer(answers, enabled_features)
            codes_to_answers[code] = answer

        return codes_to_answers

    def _generate_answer(self, answers: List[str], enabled_features: Set[str]):
        """Concatenates all answers from block and enriches answer with enabled additional features"""
        answer = Answer(text='\n'.join(answers))
        for feature in enabled_features:
            setattr(answer, feature.lower(), self.additional_features[feature](answer.text))
        return answer

