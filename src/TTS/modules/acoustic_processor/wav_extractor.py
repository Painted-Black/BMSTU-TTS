from pydub import AudioSegment
import logging
import os

from modules.allophone import Allophone


class WavExtractor:
    def __init__(self, db_path, word_pause_len, synt_pause_len):
        self.db_path = db_path
        self.allophones_dir_name = "allophones_db"
        self.cons_allophones_dir_name = "cons"
        self.vowel_allophones_dir_name = "vowels"
        self.syllables1_dir_name = "syllables1"
        self.syllables2_dir_name = "syllables2"
        self.syllables3_dir_name = "syllables3"
        self.stressed_vowel_suffix = "+"
        self.allophones_path = os.path.join(self.db_path, self.allophones_dir_name)
        self.__word_pause_len = word_pause_len
        self.__synt_pause_len = synt_pause_len

    def get_wav(self, allophones: [Allophone], mode: int) -> AudioSegment:
        """
        :param allophones
            массив аллофонов, который нужно преобразовать в wav
        :param mode
            0 -- ищем аллофоны
            1 -- ищем слоговой комплекс 1-го типа
            2 -- ищем слоговой комплекс 2-го типа
            3 -- ищем слоговой комплекс 3-го типа
        """
        if mode == 0:
            final_audio = AudioSegment.empty()
            for allophone in allophones:
                cur_wav = self.__get_allophone(allophone)
                if cur_wav is not None:
                    final_audio += cur_wav
            return final_audio
        elif mode == 1:
            final_audio = self.__get_syllable(allophones, self.syllables1_dir_name)
            return final_audio
        elif mode == 2:
            final_audio = self.__get_syllable(allophones, self.syllables2_dir_name)
            return final_audio
        elif mode == 3:
            final_audio = self.__get_syllable(allophones, self.syllables3_dir_name)
            return final_audio
        else:
            logging.error("WavExtractor:get_wav(): unknown mode")
            return None

    def __get_syllable(self, syllable: [Allophone], dir_name) -> AudioSegment:
        final_audio = AudioSegment.empty()
        filename = self.__get_syllable_file_name(syllable)
        full_path = os.path.join(self.allophones_path, dir_name, filename + ".wav")
        try:
            final_audio = AudioSegment.from_wav(full_path)
        except FileNotFoundError:
            logging.warning("No allophone {0} found at {1}".format(str(filename), full_path))
            final_audio = None
        return final_audio

    def __get_syllable_file_name(self, syllable: [Allophone]) -> str:
        name = ""
        for allophone in syllable:
            name += str(allophone)
        return name

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
