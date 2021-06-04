from modules.sentence import Sentence
from pymorphy2.tagset import OpencorporaTag
from pymorphy2 import MorphAnalyzer

WordsDelim = "_"
SyntDelim = "#"


class SentenceToSyntagmaConverter:
    __Delims = [";", ":", ",", "-", "(", ")", '"', "«", ",-", ".", "!", "...", "?"]

    @staticmethod
    def convert(sentences: [Sentence]) -> [str]:
        ma = MorphAnalyzer()
        result = []
        for sent in sentences:
            syntagma = ""
            n = len(sent.phonetic_words)
            for i in range(n):
                word = sent.phonetic_words[i]
                tag = ma.parse(word)[0]
                if tag.tag.__repr__() != "OpencorporaTag('PNCT')" or \
                        tag.normal_form not in SentenceToSyntagmaConverter.__Delims:
                    syntagma += word
                    if i != n - 1:
                        syntagma += WordsDelim
                else:
                    syntagma += SyntDelim
                    result.append(syntagma)
                    syntagma = ""
            syntagma += SyntDelim
            result.append(syntagma)
        result = SentenceToSyntagmaConverter.__clear(result)
        return result

    @staticmethod
    def __clear(syntagmas: [str]) -> [str]:
        new_synts = []
        n = len(syntagmas)
        for i in range(n):
            s = syntagmas[i].replace("_#", "#")
            if s != "#" and s != "_":
                new_synts.append(s)
        return new_synts

    @staticmethod
    def __parse_sents(sents: [Sentence]) -> [str]:
        diff = 0
        result = []
        for sent in sents:
            punct = sent.punct_words
            syntagma = ""
            n = len(punct)
            for i in range(n):
                if punct[i] in SentenceToSyntagmaConverter.__Delims:
                    syntagma += SyntDelim
                    result.append(syntagma)
                    syntagma = ""
                    diff += 1
                else:
                    word = sent.phonetic_words[i - diff]
                    syntagma += word
                    syntagma += WordsDelim
            syntagma += SyntDelim
            result.append(syntagma)
