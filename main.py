from loader.fs_doc_interviews_loader import FsDocInterviewsLoader
from mapper.fs_xls_questions_mapper import FsXlsQuestionsMapper
from extensions import DocumentExtensions
from parser.txt_interview_parser import TxtInterviewParser
from interview import ParsedInterview
from typing import List


if __name__ == '__main__':
    interviews_loader = FsDocInterviewsLoader(dir_path='interviews', extension=DocumentExtensions.HAS_X)
    interview_parser = TxtInterviewParser()
    interviews: List[ParsedInterview] = []
    for _interview in interviews_loader.load():
        interviews.append(interview_parser.parse(_interview))
    questions_mapper = FsXlsQuestionsMapper('interview_code_template.xlsx')
    for _interview in interviews:
        _interview.question_to_answer = questions_mapper.match_questions(_interview.question_to_answer)
    # TableDumper
