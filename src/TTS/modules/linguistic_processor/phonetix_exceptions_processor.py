class PhonetixExceptionsProcessor:
    def __init__(self, ph_exc_db_connection):
        self.ph_exc_db_connection = ph_exc_db_connection

    def __del__(self):
        if self.ph_exc_db_connection is not None:
            self.ph_exc_db_connection.close()

    def process(self, words: []):
        pass
