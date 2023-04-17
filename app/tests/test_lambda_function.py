from app.lambda_function import lambda_handler


def test_lambda():
    lambda_handler({"message": "test"}, {"test": "test"})