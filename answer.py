import json
from dataclasses import dataclass
from typing import List, Optional
import json


@dataclass
class Answer:
    text: str
    sa: Optional[float] = None
    kw: Optional[List[str]] = None

    format_delimiter = '|'

    def __repr__(self):
        representation = self.text
        meta = {}
        if self.sa:
            meta['sa'] = self.sa
        if self.kw:
            meta['kw'] = self.kw
        if meta:
            representation = f'{representation}{self.format_delimiter}{json.dumps(meta, ensure_ascii=False)}'
        return representation


