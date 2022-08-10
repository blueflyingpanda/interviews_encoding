from mapper.questions_mapper import QuestionsMapper
from pathlib import Path
from typing import Dict, List
from codes_to_keyword import CODES_TO_KEYWORD
import re


class FsXlsQuestionsMapper(QuestionsMapper):

    """
    loads code table from filesystem in Excel workbook format
    implements QuestionsMapper interface
    """

    FIELD_FOR_QUOTES = "((Отдельно выносим сюда цитаты"

    def __init__(self, table_path: str):
        self.table_path = Path(table_path)

    def count_frequency(self, answer: str, keywords: List[str]):
        counter = 0
        for pattern in keywords:
            counter += len(re.findall(pattern, answer)) > 0  # or and as much as found
        return counter

    def find_code(self, answer: str, block: int):
        codes_frequency = {}
        answer = answer.lower()
        for c, keywords in CODES_TO_KEYWORD.items():
            if self.BLOCKS_TO_CODES[block].start <= c < self.BLOCKS_TO_CODES[block].end:
                codes_frequency[c] = self.count_frequency(answer, keywords)
        return {k: v for k, v in sorted(codes_frequency.items(), key=lambda item: item[1], reverse=True)}

    def match_questions(self, question_to_answer: Dict[str, str], block: int) -> Dict[str, str]:
        if not self.table_path.is_file():
            raise Exception('provided path to interview code table is wrong')
        ca = {}
        # i = 0
        for a in question_to_answer.values():
            a = self._remove_dialog_pattern(a)
            codes = self.find_code(answer=a, block=block)
            last_len = len(ca)
            for code in codes:
                if codes[code] < 2:
                    continue
                if code not in ca:
                    ca[code] = a
                    break
                else:
                    ca[code] += f"| {a}"
                    break
            # if i == 4:
            #     break
            # i += 1
        return ca

    @staticmethod
    def _remove_dialog_pattern(line: str) -> str:
        return line[line.find(' ') + 1:].strip()
