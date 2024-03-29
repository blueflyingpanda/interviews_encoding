from abc import ABC


class Extensions(ABC):

    NON_X = "*.{}"
    HAS_X = "*.{}x"
    BOTH = "*.{}*"


class DocumentExtensions(Extensions):
    """helper class that works as enum for extensions in FsDocBaseInterviewsLoader"""

    BASE_EXTENSION = 'doc'

    NON_X = Extensions.NON_X.format(BASE_EXTENSION)
    HAS_X = Extensions.HAS_X.format(BASE_EXTENSION)
    BOTH = Extensions.BOTH.format(BASE_EXTENSION)

    
class SpreadsheetExtensions(Extensions):
    """helper class that works as enum for extensions in FsXlsTableDumper"""

    BASE_EXTENSION = 'xls'

    NON_X = Extensions.NON_X.format(BASE_EXTENSION)
    HAS_X = Extensions.HAS_X.format(BASE_EXTENSION)
    BOTH = Extensions.BOTH.format(BASE_EXTENSION)
