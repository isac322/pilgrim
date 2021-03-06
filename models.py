from tortoise import fields
from tortoise.models import Model


class Answer(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(64)
    grade_name = fields.CharField(64)
    cafe_name = fields.JSONField()
    feedback = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'Answer<id:{self.id}, name:{self.name}, grade_name:{self.grade_name}, cafe_name:{self.cafe_name}>'
