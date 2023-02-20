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


@dataclass
class Translation:
    teaser_link_text: str
    blog_page_title: str
    blog_navigation_name: str
    recent_blog_posts_navigation_name: str
    archive_page_title: str
    archive_navigation_name: str
    categories_page_title: str
    categories_navigation_name: str
    tags_page_title: str
    tags_navigation_name: str
    newer_posts: str
    older_posts: str

    @property
    def as_dict(self) -> dict:
        return asdict(self)
