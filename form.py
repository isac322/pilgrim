from typing import Optional

from pydantic import BaseModel, conset, constr


class QuizForm(BaseModel):
    grade_name: int
    name: constr(min_length=1)
    cafe_name: conset(int, min_items=1, max_items=2)
    feedback: Optional[str]
