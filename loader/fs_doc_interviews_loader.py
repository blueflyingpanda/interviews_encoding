import docx2txt
from pathlib import Path
from typing import Iterable

from exceptions import LoaderException
from loader.interviews_loader import BaseInterviewsLoader
from interview import RawInterview


class FsDocBaseInterviewsLoader(BaseInterviewsLoader):

    """
    loads interviews from filesystem in Word document format
    implements BaseInterviewsLoader interface
    """

    def __init__(self, dir_path: str, extension: str):
        self.interviews_path = Path(dir_path)
        self.extension_pattern = extension

    def load(self) -> Iterable[RawInterview]:
        if not self.interviews_path.is_dir():
            raise LoaderException('Provided path to interviews folder is wrong')
        for interview in self.interviews_path.glob(self.extension_pattern):
            if interview.name.startswith('~$'):  # maintains temporary information about the state of the document
                continue
            yield RawInterview(code=interview.name, content=docx2txt.process(interview))
