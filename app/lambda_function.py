from app.src.schemas.input_event_schema import InputTest
from aws_lambda_powertools.utilities.parser import parse
import pymysql

def lambda_handler(event, context):
    parsed_payload = parse(event=event, model=InputTest)
    connection = pymysql.connect(
                    host="life-manager.cb0yj0kskzwr.us-east-1.rds.amazonaws.com",
                    user="lifemanager",
                    password="dbpassword",
                    database="lifemanger",
                    port=5432,
                    cursorclass=pymysql.cursors.DictCursor
                )
    connection.close()
    return { "statusCode": "200", "message": "É nóis", "payload": parsed_payload.message}