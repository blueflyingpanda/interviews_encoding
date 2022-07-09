from mapper.questions_mapper import QuestionsMapper
from pathlib import Path
from typing import Dict
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class FsXlsQuestionsMapper(QuestionsMapper):

    """
    loads code table from filesystem in Excel workbook format
    implements QuestionsMapper interface
    """

    FIELD_FOR_QUOTES = "((Отдельно выносим сюда цитаты"

    def __init__(self, table_path: str):
        self.table_path = Path(table_path)
        self._questions = None
        self._embeddings = None
        self.model = SentenceTransformer('sentence-transformers/LaBSE')

    @property
    def questions(self):
        if self._questions is None:
            self._questions = list(pd.read_excel(self.table_path).iterrows())[0][1][3:]
            self._questions = list((q for q in self._questions if not q.startswith(self.FIELD_FOR_QUOTES)))
        return self._questions

    @property
    def embeddings(self):
        if self._embeddings is None:
            self._embeddings = self.model.encode(self.questions)
        return self._embeddings

    def match_questions(self, question_to_answer: Dict[str, str]) -> Dict[str, str]:
        if not self.table_path.is_file():
            raise Exception('provided path to interview code table is wrong')
        table_question_index = 0
        qa = {}
        for q in question_to_answer:
            cosim = cosine_similarity(
                    self.embeddings,
                    self.model.encode(self._remove_dialog_pattern(q)).reshape(1, -1))
            cosim = list(cosim)
            max_index = cosim.index(max(cosim))
            while self.questions[max_index] in qa and len(cosim):
                cosim.pop(max_index)
                if len(cosim):
                    max_index = cosim.index(max(cosim))
            if len(cosim):
                qa[self.questions[max_index]] = self._remove_dialog_pattern(question_to_answer[q])
        return qa

    @staticmethod
    def _remove_dialog_pattern(line: str) -> str:
        return line[line.find(' ') + 1:].strip()
