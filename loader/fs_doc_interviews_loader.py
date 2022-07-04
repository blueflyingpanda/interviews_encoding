import docx2txt
from pathlib import Path
from typing import Iterable
from loader.interviews_loader import InterviewsLoader
from interview import RawInterview


class FsDocInterviewsLoader(InterviewsLoader):

    """
    loads interviews from filesystem in Word document format
    implements InterviewsLoader interface
    """

    def __init__(self, dir_path: str, extension: str):
        self.interviews_path = Path(dir_path)
        self.extension_pattern = extension

    def load(self) -> Iterable[RawInterview]:
        if not self.interviews_path.is_dir():
            raise Exception('provided path to interview folder is wrong')
        for interview in self.interviews_path.glob(self.extension_pattern):
            yield RawInterview(code=interview.name, content=docx2txt.process(interview))
