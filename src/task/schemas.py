from typing import List, Union

from pydantic import BaseModel, validator, Field
from datetime import datetime
# from pydantic.datetime_parse import parse_datetime
from sqlalchemy.orm import Relationship


class TaskCreate(BaseModel):
    slip_time: int = 10
    priority: str = Field(..., example="high")

    class Config:
        from_attributes = True

    @validator("priority", pre=True)
    def toppings_validate(cls, date):
        if date not in ["high", "medium", "low"]:
            raise ValueError('priority supposed to be "high" or "medium" or "low"')
        return date

class TaskIdView(BaseModel):
    id: str

    class Config:
        from_attributes = True

class TaskView(TaskIdView):
    status: str
    execution_time: Union[float, None] = None


