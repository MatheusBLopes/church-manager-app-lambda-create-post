from app.src.schemas.input_event_schema import InputTest


def lambda_handler(event, context):
    parsed_payload = InputTest(event)
    return { "statusCode": "200", "message": "É nóis", "payload": parsed_payload.message}