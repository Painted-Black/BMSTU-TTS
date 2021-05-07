from modules.sentence import Sentence

WordsDelim = "_"
SyntDelim = "#"


class SentenceToSyntagmaConverter:
    @staticmethod
    def convert(sentences: [Sentence]) -> [str]:
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
