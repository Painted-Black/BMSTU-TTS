from razdel import sentenize
from modules.sentence import Sentence


class SentenceExtractor:
    @staticmethod
    def split_sentences(text: str) -> []:
        buf = sentenize(text)
        buf = list(buf)
        sent = []
        for i in range(len(buf)):
            s = Sentence(buf[i].text)
            sent.append(s)
        return sent
