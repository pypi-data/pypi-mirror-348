from pydantic import BaseModel, model_validator
from enum import Enum


class NewsStatus(str, Enum):
    PUBLISHED = "published"
    NEW = "new"
    FAILED = "failed"


class News(BaseModel):
    title: str
    summary: str = ""
    content: str = ""
    status: NewsStatus = NewsStatus.NEW

    @model_validator(mode='before')
    @classmethod
    def remove_non_bmp(cls, values):
        for field in ['title', 'summary', 'content']:
            if field in values:
                values[field] = ''.join(
                    c for c in values[field] if ord(c) <= 0xFFFF
                    )
        return values
