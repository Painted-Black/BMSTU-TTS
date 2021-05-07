from modules.allophone import Allophone
from modules.phonetic_processor.syllabic_complex1_unit import SyllabicComplex1Unit
from modules.phonetic_processor.syllabic_complex import SyllabicUnit


class SyllabicComplex2Unit(SyllabicUnit):
    def __init__(self):
        super().__init__()
        self.__sc1u = SyllabicComplex1Unit()

    def process_by_word(self, allophones: [Allophone]) -> [[[Allophone]]]:
        syllables = self.__sc1u.process_by_word(allophones)
        self._correct_sonants(syllables)
        return syllables

    def process_by_sintagmas(self, allophones: [Allophone]) -> [[[Allophone]]]:
        syllables = self.__sc1u.process_by_sintagmas(allophones)
        self._correct_sonants(syllables)
        return syllables
