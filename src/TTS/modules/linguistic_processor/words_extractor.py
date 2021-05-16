from modules.sentence import Sentence
from nltk import word_tokenize
from modules.linguistic_processor.symbols_base import contains_only_consonants, count_vowels
from modules.linguistic_processor.symbols_base import PunctuationMarks


class WordsExtractor:
    InitialsPattern = r"((\b[А-ЯЁ]\.) *([А-ЯЁ]\b\.)?)"
    HyphenParticlePattern = r"(-[а-яё]+)"

    def split_words(self, sents: [Sentence]):
        n = len(sents)
        for i in range(n):
            buf = word_tokenize(sents[i].raw_data)
            corrected_buf = []
            for b in buf:
                if not (len(b) == 1 and b[0] in PunctuationMarks):
                    corrected_buf.append(b)
                sents[i].words = corrected_buf

    @staticmethod
    def is_service_word(word: str, part_of_speech: str) -> bool:
        if word == "либо" or word == "нибудь":
            return True
        if part_of_speech == "PREP":
            if contains_only_consonants(word):
                return True
            if count_vowels(word) == 1:
                return True
        if part_of_speech == "PRCL" or part_of_speech == "CONJ":
            if word == "б" or word == "ж" or word == "ль":
                return True
            if count_vowels(word) == 1:
                return True
        return False
