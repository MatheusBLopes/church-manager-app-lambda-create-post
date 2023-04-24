from app.src.schemas.input_event_schema import InputTest
from aws_lambda_powertools.utilities.parser import parse
from app.src.ports.database_repository import Database

def lambda_handler(event, context):
    parsed_payload = parse(event=event, model=InputTest)
    db = Database()
    return { "statusCode": "200", "message": "É nóis", "payload": parsed_payload.message}