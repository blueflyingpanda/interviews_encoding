from loader.fs_doc_interviews_loader import FsDocInterviewsLoader
from mapper.fs_xls_questions_mapper import FsXlsQuestionsMapper
from extensions import DocumentExtensions
from parser.txt_interview_parser import TxtInterviewParser
from interview import ParsedInterview
from dumper.fs_xls_interviews_dumper import FsXlsInterviewsDumper
from typing import List


if __name__ == '__main__':
    interviews_loader = FsDocInterviewsLoader(dir_path='interviews', extension=DocumentExtensions.HAS_X)
    interview_parser = TxtInterviewParser()
    interviews: List[ParsedInterview] = []
    for _interview in interviews_loader.load():
        interviews.append(interview_parser.parse(_interview))

    questions_mapper = FsXlsQuestionsMapper('interview_code_template.xlsx')
    for _interview in interviews:
        _interview.code_to_answer = questions_mapper.match_questions(_interview.qa_block1, block=1)
        _interview.code_to_answer.update(questions_mapper.match_questions(_interview.qa_block2, block=2))
        _interview.code_to_answer.update(questions_mapper.match_questions(_interview.qa_block3, block=3))

    interviews_dumper = FsXlsInterviewsDumper(table_path='interview_code.xlsx',
                                              template_path='interview_code_template.xlsx')
    interviews_dumper.dump(interviews)
