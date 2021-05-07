from modules.allophone import Allophone
from modules.phonetic_processor.syllabic_complex import SyllabicUnit
from modules.phonetic_processor.syllabic_complex2_unit import SyllabicComplex2Unit


class SyllabicComplex3Unit(SyllabicUnit):
    def __init__(self):
        super().__init__()
        self.__sc2u = SyllabicComplex2Unit()

    def process_by_word(self, allophones: [Allophone]) -> [[[Allophone]]]:
        syllables = self.__sc2u.process_by_word(allophones)
        self.__process(syllables)
        print(syllables)

    def __process(self, syllables: [[[Allophone]]]):
        self.__correct_sonant_not_stressed(syllables)
        self._correct_double_vowels(syllables)
        self._correct_j_vowel(syllables)
        self._correct_single_vowel(syllables)
        self._correct_sonants(syllables)

    def process_by_sintagmas(self, allophones: [Allophone]) -> [[[Allophone]]]:
        syllables = self.__sc2u.process_by_sintagmas(allophones)
        self.__process(syllables)
        print(syllables)
        return syllables

    def __correct_sonant_not_stressed(self, syllables: [[[Allophone]]]) -> [[[Allophone]]]:
        n = len(syllables)
        for i in range(n):
            j = 0
            while j < len(syllables[i]):
                cur_syllable, next_syllable = self._get_cur_next(syllables[i], j)
                if next_syllable is not None:
                    p = len(next_syllable)
                    cur_last = self._get_last(cur_syllable)
                    if cur_last is not None and cur_last.is_vowel() and p != 0:
                        to_add, new_next = self.__remove_first_sonant(next_syllable)
                        syllables[i][j] += to_add
                        syllables[i][j + 1] = new_next
                        if len(new_next) == 0:
                            syllables[i] = syllables[i][:j + 1] + syllables[i][j + 2:]
                            j -= 1
                j += 1

    def __remove_first_sonant(self, syllable: [Allophone]):
        to_remove = []
        idx = None
        n = len(syllable)
        for i in range(n):
            allophone = syllable[i]
            if i < n - 1:
                next_allophone = syllable[i+1]
                if allophone.is_consonant() and \
                    allophone.phoneme in self.Sonants and \
                    next_allophone.is_vowel() and \
                    not next_allophone.is_stressed():
                    to_remove.append(allophone)
                    to_remove.append(next_allophone)
                    idx = i + 1
                break
            else:
                break
        if idx is not None:
            new_syllable = syllable[idx + 1:]
        else:
            new_syllable = syllable
        return to_remove, new_syllable
