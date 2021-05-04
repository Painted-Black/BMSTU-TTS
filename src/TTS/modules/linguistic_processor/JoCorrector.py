import logging


class JoCorrector:
    def __init__(self, jo_db_connection):
        self.jo_db_connection = jo_db_connection

    def __del__(self):
        if self.jo_db_connection is not None:
            self.jo_db_connection.close()

    def correct(self, words: []):
        if self.jo_db_connection is None:
            logging.error("Unable to connect to jo database")
            return None
        n = len(words)
        for i in range(n):
            pass
