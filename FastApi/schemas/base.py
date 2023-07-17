from pydantic import BaseModel, Field


class Success(BaseModel):
    result: bool = Field(default=True, )
