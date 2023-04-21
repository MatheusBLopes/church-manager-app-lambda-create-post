import pymysql
from aws_lambda_powertools import Logger

logger = Logger()

class DatabaseConnectionSingleton:
    __connection_instance = None

    def __init__(self):
        if DatabaseConnectionSingleton.__connection_instance is None:
            logger.info("Conectando ao banco de dados")
            try:
                connection = pymysql.connect(
                    host="life-manager.cb0yj0kskzwr.us-east-1.rds.amazonaws.com",
                    user="dbuser",
                    password="dbpassword",
                    database="LifeManagerDb",
                    port=5432,
                    cursorclass=pymysql.cursors.DictCursor
                )
            except Exception as error:
                logger.info(f"Erro ao conectar no banco de dados {error}")
                raise error

            DatabaseConnectionSingleton.__connection_instance = connection
        else:
            raise Exception("You can't instanciate another database connection")
    
    @staticmethod
    def get_instance():
        if DatabaseConnectionSingleton.__connection_instance is None:
            DatabaseConnectionSingleton()
        
        return DatabaseConnectionSingleton.__connection_instance

class Database():
    def __init__(self):
        self.connection = DatabaseConnectionSingleton.get_instance()
        self.cursor = self.connection.cursor()
    
    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        return result

    def save(self, insert_stmt: str, data: dict):
        try:
            self.cursor.execute(insert_stmt, data)
            result = self.cursor.lastrowid
            self.connection.commit()
        
        except Exception as error:
            raise error

        return result

    def update(self, update_stmt: str, data: dict):
        try:
            result = self.cursor.execute(update_stmt, data)
        
        except Exception as error:
            raise error
        
        return result

    def delete(self, delete_stmt, data):
        try:
            self.cursor.execute(delete_stmt, data)
            self.connection.commit()
        except Exception as error:
            raise error
        
        return True
