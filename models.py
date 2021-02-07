from pydantic import BaseModel, conint, constr


class QuizForm(BaseModel):
    grade: conint(gt=0, lt=15)
    name: str
    phone_number: constr(regex=r'^01[016789](:?[0-9]{3,4})(:?[0-9]{4})$')
    answer: str
