from src.schemas.input_event_schema import InputTest
from aws_lambda_powertools.utilities.parser import parse

def lambda_handler(event, context):
    parsed_payload = parse(event=event, model=InputTest)
    return { "statusCode": "200", "message": "É nóis", "payload": parsed_payload}