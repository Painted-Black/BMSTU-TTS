from modules.allophone import Allophone
from modules.phonetic_processor.open_syllable_unit import OpenSyllableUnit
from modules.phonetic_processor.syllabic_complex import SyllabicUnit


class SyllabicComplex1Unit(SyllabicUnit):
    def __init__(self):
        super().__init__()
        self.__osu = OpenSyllableUnit()

    def process_by_word(self, allophones: [Allophone]) -> [[[Allophone]]]:
        words = self._split_words(allophones)
        syllables = self.__process(words)
        return syllables

    def __process(self, words: [[Allophone]]) -> [[[Allophone]]]:
        syllables = []
        for word in words:
            cur_syllables = self.__osu.process(word)
            syllables.append(cur_syllables)
        self._correct_double_vowels(syllables)
        self._correct_j_vowel(syllables)
        self._correct_single_vowel(syllables)
        return syllables

    def process_by_sintagmas(self, allophones: [Allophone]) -> [[[Allophone]]]:
        words = self._split_syntagmas(allophones)
        syllables = self.__process(words)
        return syllables
