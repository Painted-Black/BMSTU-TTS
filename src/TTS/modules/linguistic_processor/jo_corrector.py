import logging
from pymorphy2 import MorphAnalyzer
import pickle
from pymorphy2.tagset import OpencorporaTag


class JoCorrector:
    def __init__(self):
        self.morph_analyzer = MorphAnalyzer()

    def correct(self, words: []) -> []:
        n = len(words)
        for i in range(n):
            word = str(words[i])
            if word.__contains__("е") or word.__contains__("Е"):
                item = self.morph_analyzer.parse(word)[0]
                corrected_jo = item.word
                if word != corrected_jo:
                    words[i] = corrected_jo
        return words
