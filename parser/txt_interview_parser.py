from parser.interview_parser import InterviewParser
from interview import RawInterview, ParsedInterview
from typing import Dict
import re
import logging


class TxtInterviewParser(InterviewParser):

    """
    parses interviews in text format (.txt)
    """

    def parse(self, raw_interview: RawInterview) -> ParsedInterview:
        parsed_interview = ParsedInterview(
            code=raw_interview.code,
            content=None,  # content will be parsed and no longer required
            question_to_answer={},
            code_to_answer={},
            qa_block1={},
            qa_block2={},
            qa_block3={}
        )
        start_index = self._get_interview_start_index(raw_interview.content)
        # ' ' - weird values that appear when converting doc to txt
        header = raw_interview.content[:start_index].replace(' ', '')
        body = raw_interview.content[start_index:].replace(' ', '')
        self._add_meta_from_header(header, parsed_interview)
        parsed_interview.question_to_answer = self._parse_answers_to_questions(body)

        b1b2_separator_pos = body.find(self.B1B2_SEPARATOR)
        b2_question_start = body.rfind(self.INTERVIEWER_LABEL, 0, b1b2_separator_pos)
        block1 = body[:b2_question_start]
        b2b3_separator_pos = -1
        for sep in self.B2B3_SEPARATORS:
            b2b3_separator_pos = body.find(sep, b1b2_separator_pos)
            if b2b3_separator_pos != -1:
                break
        block3_is_empty = False
        if b2b3_separator_pos == -1:
            block3 = ''
            logging.warning(f'empty block3 for {raw_interview.code}')
            block3_is_empty = True
        if block3_is_empty:
            block2 = body[b2_question_start:]
        else:
            b3_question_start = body.rfind(self.INTERVIEWER_LABEL, 0, b2b3_separator_pos)
            block2 = body[b2_question_start:b3_question_start]
            block3 = body[b3_question_start:]
            parsed_interview.qa_block3 = self._parse_answers_to_questions(block3[3:])

        parsed_interview.qa_block1 = self._parse_answers_to_questions(block1)
        parsed_interview.qa_block2 = self._parse_answers_to_questions(block2[3:])

        return parsed_interview

    def _get_interview_start_index(self, content: str) -> int:
        start_index = float('inf')
        content = content.lower()
        for interview_start in self.INTERVIEW_STARTS:
            tmp = content.find(interview_start)
            if tmp < start_index:
                start_index = tmp
        return start_index

    def _add_meta_from_header(self, header: str, parsed_interview: ParsedInterview):
        header = header.replace(':', ' ')
        header = re.sub(r'\((.+?)\)', '', header)
        header = re.sub(r'\[(.+?)\]', '', header)
        tokens = [token.strip() for token in header.split('\n') if token.strip()]
        for field in self.HEADER_FIELDS:
            setattr(parsed_interview, field, tokens[tokens.index(self.HEADER_FIELDS[field]) + 1])

    def _parse_answers_to_questions(self, body: str) -> Dict[str, str]:
        qa = {}
        if not body:
            return qa
        body = re.sub(r'\[\d{2}:\d{2}:\d{2}]', '', body)
        tokens = [token.strip() for token in body.split('\n') if token.strip()]
        tokens[0] = self.INTERVIEWER_LABEL + ' ' + tokens[0]
        last_question = tokens[0]
        for i in range(len(tokens)):
            if tokens[i].startswith(self.INTERVIEWER_LABEL):
                if i + 1 < len(tokens):
                    if tokens[i + 1].startswith(self.RESPONDENT_LABEL):
                        last_question = tokens[i]
                        qa[tokens[i]] = tokens[i + 1]
            elif not tokens[i].startswith(self.RESPONDENT_LABEL):
                qa[last_question] += " " + tokens[i]
        return qa
