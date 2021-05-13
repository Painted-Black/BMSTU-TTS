from modules.phonetic_processor.letter_phoneme_transcriptor import LetterPhonemeTranscriptor
from modules.phonetic_processor.phoneme_allophone_transcriptor import PhonemeAllophoneTranscriptor


class PhoneticProcessor:
    def __init__(self):
        self.__lft = LetterPhonemeTranscriptor()
        self.__pat = PhonemeAllophoneTranscriptor()

    def process(self, text):
        phonemes = self.__lft.transcript(text)
        allophones = self.__pat.transcript(phonemes)
        return allophones
