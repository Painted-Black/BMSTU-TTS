from modules.linguistic_processor.sentence import Sentence
from nltk import word_tokenize


class WordsExtractor:
    InitialsPattern = r"((\b[А-ЯЁ]\.) *([А-ЯЁ]\b\.)?)"

    def split_words(self, sents: [Sentence]):
        n = len(sents)
        for i in range(n):
            buf = word_tokenize(sents[i].raw_data)
            buf = self.__remove_punct_marks(buf)
            buf = self.__lower_words(buf)
            sents[i].words = buf

    def __lower_words(self, words: [str]) -> [str]:
        for i in range(len(words)):
            words[i] = words[i].lower()
        return words

    def __remove_punct_marks(self, words: [str]) -> [str]:
        res = []
        for w in words:
            if w.isalpha() is True:
                res.append(w)
        return res
