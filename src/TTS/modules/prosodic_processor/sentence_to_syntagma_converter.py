from modules.sentence import Sentence

WordsDelim = "_"
SyntDelim = "#"


class SentenceToSyntagmaConverter:
    __Delims = [";", ":", ",", "-", "(", ")", '"', "«", ",-"]
    @staticmethod
    def convert(sentences: [Sentence]) -> [str]:
        SentenceToSyntagmaConverter.__parse_sents(sentences)
        result = []
        for sent in sentences:
            syntagma = ""
            n = len(sent.phonetic_words)
            for i in range(n):
                word = sent.phonetic_words[i]
                syntagma += word
                if i != n - 1:
                    syntagma += WordsDelim
            syntagma += SyntDelim
            result.append(syntagma)
        return result

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
                    word = sent.phonetic_words[i-diff]
                    syntagma += word
                    syntagma += WordsDelim
            syntagma += SyntDelim
            result.append(syntagma)
