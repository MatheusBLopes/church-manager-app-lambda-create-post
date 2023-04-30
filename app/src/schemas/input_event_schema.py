from aws_lambda_powertools.utilities.parser import BaseModel

class CreatePostInputSchema(BaseModel):
    day_of_the_week: str
    date: str
    preacher: str
    theme: str