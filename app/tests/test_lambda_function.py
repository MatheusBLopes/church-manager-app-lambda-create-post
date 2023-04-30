from app.lambda_function import lambda_handler


def test_lambda():
    response = lambda_handler(
        {
            "day_of_the_week": "SÁBADO",
            "date": "29 ABR | à 9:00",
            "preacher": "Pregador: Matheus B. Lopes",
            "theme": "Tema: Hebraico Antigo"
        }, context={}
    )