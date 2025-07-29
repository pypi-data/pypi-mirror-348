from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    class Config:
        populate_by_name = True


class PageRequest(BaseSchema):
    page: int = Field(default=0, alias="page")
    page_size: int = Field(default=0, alias="pageSize")
    keyword: str = Field(default="", alias="keyword")
