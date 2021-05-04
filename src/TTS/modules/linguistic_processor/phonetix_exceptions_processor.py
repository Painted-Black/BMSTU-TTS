import logging
import pickle


class PhonetixExceptionsProcessor:
    def __init__(self, ph_exc_db_connection):
        self.ph_exc_db_connection = ph_exc_db_connection

    def __del__(self):
        if self.ph_exc_db_connection is not None:
            self.ph_exc_db_connection.close()

    def process(self, words: []):
        if self.ph_exc_db_connection is None:
            logging.error("Unable to connect to phonetic exceptions database")
            return None
        n = len(words)
        for i in range(n):
            word = str(words[i])
            word, pos = self.__remove_symbs(word)
            pronounce = self.ph_exc_db_connection.read(pickle.dumps(word))
            if pronounce is not None:
                pronounce = pickle.loads(pronounce)
                pronounce = self.__return_symbs(pronounce, pos)
                words[i] = pronounce
        return words

    def __remove_symbs(self, word):
        pos = {}
        idx = word.rfind('+')
        while idx != -1:
            pos[idx] = '+'
            idx = word.find('+', idx+1)

        idx = word.rfind('=')
        while idx != -1:
            pos[idx] = '='
            idx = word.find('=', idx+1)
        word = word.replace('+', '')
        word = word.replace('=', '')
        return word, pos

    def __return_symbs(self, word, positions: {}):
        keys = positions.keys()
        for key in keys:
            symb = positions[key]
            word = word[:key] + symb + word[key:]
        return word
