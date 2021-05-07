from modules.phonetic_processor.letter_phoneme_transcriptor import LetterPhonemeTranscriptor
from modules.phonetic_processor.phoneme_allophone_transcriptor import PhonemeAllophoneTranscriptor
from modules.phonetic_processor.syllabic_complex1_unit import SyllabicComplex1Unit
from modules.phonetic_processor.syllabic_complex2_unit import SyllabicComplex2Unit
from modules.phonetic_processor.syllabic_complex3_unit import SyllabicComplex3Unit


class PhoneticProcessor:
    def __init__(self):
        self.__lft = LetterPhonemeTranscriptor()
        self.__pat = PhonemeAllophoneTranscriptor()
        self.__sc3 = SyllabicComplex1Unit()

    def process(self, text):
        phonemes = self.__lft.transcript(text)
        allophones = self.__pat.transcript(phonemes)
        syllable_1 = self.__sc3.process_by_word(allophones)
        print(syllable_1)
        return allophones
