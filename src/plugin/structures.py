from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from typing import List
from typing import Optional
from typing import Union


@dataclass
class BlogPost:
    """Single blog post data container"""

    title: str
    date: datetime
    path: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
    category: Optional[str]
    slug: Union[str, None] = None
    teaser: str = ""
    is_teaser: bool = False

    @property
    def as_dict(self) -> dict:
        return asdict(self)
