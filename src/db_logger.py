import sqlite3
from exception import CustomException
from log import logging
import sys
import datetime
import os
class RequestLogger:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), "data", "requests_database.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        try:
            connection = sqlite3.connect(self.db_path)
            cur = connection.cursor()
            table_create = """
                CREATE TABLE IF NOT EXISTS REQUESTS(
                ID_REQUEST INTEGER PRIMARY KEY AUTOINCREMENT,
                REQUEST_TIME DATETIME,
                REQUEST VARCHAR(255),
                NUMBER_OF_ANSWERS INTEGER NOT NULL,
                BEST_ANSWER_ID VARCHAR(20),
                BEST_SCORE REAL,
                RESULT_PREVIEW VARCHAR(150)
                );
            """
            cur.execute(table_create)
            cur.close()
            connection.commit()
            connection.close()
            logging.info("Connection to the database was made")
        except Exception as e:
            CustomException(e,sys)
    def insertRequest(self, request, numberOfanswers=0, BestAnswer=None, BestScore=None, preview=None):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cur_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insertion = """
                INSERT INTO REQUESTS (REQUEST_TIME, REQUEST, NUMBER_OF_ANSWERS, BEST_ANSWER_ID, BEST_SCORE, RESULT_PREVIEW)
                VALUES (?,?,?,?,?,?)
            """
            cursor.execute(insertion, (cur_date, request, numberOfanswers, BestAnswer, BestScore, preview))
            cursor.close()
            connection.commit()
            connection.close()
        except Exception as e:
            CustomException(e,sys)
    def selectRequests(self, id=None):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            if id == None:
                select = """
                        SELECT * FROM REQUESTS
                    """
                cursor.execute(select)
            else:
                select = """
                    SELECT * FROM REQUESTS
                    WHERE ID_REQUEST=?
                    """
                cursor.execute(select,(id,))
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return data
        except Exception as e:
            CustomException(e,sys)