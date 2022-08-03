from mapper.questions_mapper import QuestionsMapper
from pathlib import Path
from typing import Dict, List
from codes_to_keyword import CODES_TO_KEYWORD
import re
import pandas as pd
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity


class FsXlsQuestionsMapper(QuestionsMapper):

    """
    loads code table from filesystem in Excel workbook format
    implements QuestionsMapper interface
    """

    FIELD_FOR_QUOTES = "((Отдельно выносим сюда цитаты"

    def __init__(self, table_path: str):
        self.table_path = Path(table_path)
        # self._questions = None
        # self._embeddings = None
        # self.model = SentenceTransformer('sentence-transformers/LaBSE')

    # @property
    # def questions(self):
    #     if self._questions is None:
    #         self._questions = list(pd.read_excel(self.table_path).iterrows())[0][1][3:]
    #         self._questions = list((q for q in self._questions if not q.startswith(self.FIELD_FOR_QUOTES)))
    #     return self._questions

    # @property
    # def embeddings(self):
    #     if self._embeddings is None:
    #         self._embeddings = self.model.encode(self.questions)
    #     return self._embeddings

    def count_frequency(self, answer: str, keywords: List[str]):
        counter = 0
        for pattern in keywords:
            counter += len(re.findall(pattern, answer)) > 0
        return counter

    def find_code(self, answer: str):
        codes_frequency = {}
        answer = answer.lower()
        for c, keywords in CODES_TO_KEYWORD.items():
            codes_frequency[c] = self.count_frequency(answer, keywords)
        return {k: v for k, v in sorted(codes_frequency.items(), key=lambda item: item[1], reverse=True)}

    def match_questions(self, question_to_answer: Dict[str, str]) -> Dict[str, str]:
        if not self.table_path.is_file():
            raise Exception('provided path to interview code table is wrong')
        ca = {}
        i = 0
        for a in question_to_answer.values():
            a = self._remove_dialog_pattern(a)
            codes = self.find_code(answer=a)
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
            if i == 4:
                break
            i += 1
            # if last_len == len(ca):
            #     raise Exception(f'No code was assigned to answer {a}')
            # else:
            #     ca[code] += a
        return ca

    @staticmethod
    def _remove_dialog_pattern(line: str) -> str:
        return line[line.find(' ') + 1:].strip()
