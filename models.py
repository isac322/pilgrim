from typing import Optional, Sequence, Union

from pydantic import BaseModel, constr


class QuizForm(BaseModel):
    grade_name: constr(min_length=1)
    name: constr(min_length=1)
    cafe_name: Union[Sequence[str], constr(min_length=1)]
    feedback: Optional[str]
