from pydub import AudioSegment
import logging
import os


class WavExtractor:
    def __init__(self, db_path, word_pause_len, synt_pause_len):
        self.db_path = db_path
        self.allophones_dir_name = "allophones_db"
        self.cons_allophones_dir_name = "cons"
        self.vowel_allophones_dir_name = "vowels"
        self.stressed_vowel_suffix = "+"
        self.allophones_path = os.path.join(self.db_path, self.allophones_dir_name)
        self.__word_pause_len = word_pause_len
        self.__synt_pause_len = synt_pause_len

    def get_wav(self, allophone, _type: int) -> AudioSegment:
        '''
        :param _type:
            0 -- аллофон
            1 -- слоговой комплекс 1-го типа
            2 -- слоговой комплекс 2-го типа
            3 -- слоговой комплекс 3-го типа
        '''
        res = None
        if _type == 0:
            res = self.__get_allophone(allophone)
        return res

    def __get_allophone(self, allophone) -> AudioSegment:
        wav = None
        if allophone.is_vowel():
            wav = self.__get_vowel(allophone)
        elif allophone.is_consonant():
            wav = self.__get_cons(allophone)
        else:  # пауза
            wav = self.__get_pause(allophone)
        return wav

    def __get_pause(self, allophone) -> AudioSegment:
        if allophone.is_word_pause():
            wav = AudioSegment.silent(duration=self.__word_pause_len)
        else:
            wav = AudioSegment.silent(duration=self.__synt_pause_len)
        return wav

    def __get_cons(self, allophone) -> AudioSegment:
        wav = None
        cons_dir = allophone.phoneme
        full_path = os.path.join(self.allophones_path, self.cons_allophones_dir_name, cons_dir, str(allophone) + ".wav")
        try:
            wav = AudioSegment.from_wav(full_path)
        except FileNotFoundError:
            logging.error("No allophone {0} found at {1}".format(str(allophone), full_path))
        return wav

    def __get_vowel(self, allophone) -> AudioSegment:
        wav = None
        vowel_dir = allophone.phoneme
        if allophone.is_stressed():
            vowel_dir += self.stressed_vowel_suffix
        full_path = os.path.join(self.allophones_path, self.vowel_allophones_dir_name, vowel_dir, str(allophone) +
                                 ".wav")
        try:
            wav = AudioSegment.from_wav(full_path)
        except FileNotFoundError:
            logging.error("No allophone {0} found at {1}".format(str(allophone), full_path))
        return wav


class AcousticProcessor:
    def __init__(self, db_path, final_audio_path, out_format, word_pause_len, synt_pause_len):
        self.final_audio_path = final_audio_path
        self.out_format = out_format
        self.__word_pause_len = word_pause_len  # длина паузы между сегментами в синтагме в мс
        self.__syntagma_pause_len = synt_pause_len  # длина паузы между синтагмами в мс
        self.wav_extractor = WavExtractor(db_path, self.__word_pause_len, self.__syntagma_pause_len)

    word_pause_len = property()
    syntagma_pause_len = property()

    @word_pause_len.getter
    def word_pause_len(self):
        return self.__word_pause_len

    @word_pause_len.setter
    def word_pause_len(self, value):
        assert value >= 0
        self.__word_pause_len = value

    @syntagma_pause_len.getter
    def syntagma_pause_len(self):
        return self.__syntagma_pause_len

    @syntagma_pause_len.setter
    def syntagma_pause_len(self, value):
        assert value >= 0
        self.__syntagma_pause_len = value

    def process(self, allophones: []):
        final_audio = AudioSegment.empty()
        for allophone in allophones:
            cur_wav = self.wav_extractor.get_wav(allophone, 0)
            if cur_wav is not None:
                final_audio += cur_wav
        final_audio.export(self.final_audio_path, format=self.out_format)
