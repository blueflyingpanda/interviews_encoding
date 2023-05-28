from pathlib import Path
from dumper.interviews_dumper import BaseInterviewsDumper
from interview import ParsedInterview
from typing import List
import pandas as pd


class FsXlsInterviewsDumper(BaseInterviewsDumper):
    """
    dumps interviews into filesystem in Excel spreadsheet format
    implements BaseInterviewsDumper interface
    """

    def __init__(self, table_path: str, template_path: str):
        self.table_path = Path(table_path)
        self.template_path = Path(template_path)
        self._table = None

    @property
    def table(self):
        if not self._table:
            self._table = pd.read_excel(self.template_path)
        return self._table

    def dump(self, interviews: List[ParsedInterview]) -> None:
        table = self.table
        for interview in interviews:
            new_row = [interview.code, interview.date, interview.interviewer_name, interview.respondent_name,
                       interview.respondent_expertise, interview.duration]
            meta_length = len(new_row)
            new_row.extend([''] * (table.shape[1] - meta_length))
            for code, answer in interview.code_to_answer.items():
                new_row[meta_length + code - 1] = str(answer)
            table.loc[len(table.index)] = new_row
        table.to_excel(self.table_path)
