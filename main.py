from answer import Answer
from loader.fs_doc_interviews_loader import FsDocBaseInterviewsLoader
from extensions import DocumentExtensions
from parser.txt_interview_parser import TxtInterviewParser
from interview import ParsedInterview
from dumper.fs_xls_interviews_dumper import FsXlsInterviewsDumper
from formatter.fs_xls_table_formatter import FsXlsTableFormatter
from typing import List


if __name__ == '__main__':
    table_path = 'interview_code.xlsx'
    interviews_loader = FsDocBaseInterviewsLoader(dir_path='interviews', extension=DocumentExtensions.HAS_X)
    interview_parser = TxtInterviewParser(block_delimiter='==')
    interviews: List[ParsedInterview] = [interview_parser.parse(interview) for interview in interviews_loader.load()]

    interviews_dumper = FsXlsInterviewsDumper(table_path=table_path,
                                              template_path='interview_code_template.xlsx')
    interviews_dumper.dump(interviews)
    FsXlsTableFormatter.format(table_path, Answer.format_delimiter)
    print(f'Interviews encoded into {table_path}')
