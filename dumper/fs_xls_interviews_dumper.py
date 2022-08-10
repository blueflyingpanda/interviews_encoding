from pathlib import Path
from dumper.interviews_dumper import InterviewsDumper
from interview import ParsedInterview
from typing import List
import pandas as pd


class FsXlsInterviewsDumper(InterviewsDumper):
    """
    dumps interviews into filesystem in Excel spreadsheet format
    implements InterviewsDumper interface
    """

    FIELD_FOR_QUOTES = "((Отдельно выносим сюда цитаты"

    def __init__(self, table_path: str, template_path: str):
        self.table_path = Path(table_path)
        self.template_path = Path(template_path)
        self._table = None

    @property
    def table(self):
        if not self._table:
            self._table = pd.read_excel(self.template_path)
        return self._table

    def insert_fields_for_quotes(self, answers: List[str]) -> List[str]:
        answers_with_quotes = []
        guidelines_answers = list(pd.read_excel(self.template_path).iterrows())[0][1][3:]
        for a in guidelines_answers:
            if self.FIELD_FOR_QUOTES in a:
                answers_with_quotes.append('DELETEME')
            elif answers:
                answers_with_quotes.append(answers.pop(0))
        return answers_with_quotes

    def dump(self, interviews: List[ParsedInterview]) -> None:
        table = self.table
        print(table.head())
        for interview in interviews:
            new_row = [interview.code, interview.respondent_name,
                       interview.respondent_expertise] + self.insert_fields_for_quotes(
                list(interview.question_to_answer.values()))
            while len(new_row) < 64:
                new_row.append('ERROR')
            table.loc[len(table.index)] = new_row
        table.to_excel(self.table_path)
