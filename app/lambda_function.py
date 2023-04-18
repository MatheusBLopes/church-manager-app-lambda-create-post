from app.src.schemas.input_event_schema import InputTest
from aws_lambda_powertools.utilities.parser import parse
import pymysql

def lambda_handler(event, context):
    parsed_payload = parse(event=event, model=InputTest)
    connection = pymysql.connect(
                    host="terraform-20230418224750246200000001.cnjstxqpfga2.sa-east-1.rds.amazonaws.com",
                    user="dbuser",
                    password="dbpassword",
                    database="LifeManagerDb",
                    port=5432,
                    cursorclass=pymysql.cursors.DictCursor
                )
    connection.close()
    return { "statusCode": "200", "message": "É nóis", "payload": parsed_payload.message}