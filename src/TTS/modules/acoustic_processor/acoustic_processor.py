from pydub import AudioSegment
import logging

from modules.acoustic_processor.wav_extractor import WavExtractor
from modules.allophone import Allophone
from modules.phonetic_processor.syllabic_complex1_unit import SyllabicComplex1Unit
from modules.phonetic_processor.syllabic_complex2_unit import SyllabicComplex2Unit
from modules.phonetic_processor.syllabic_complex3_unit import SyllabicComplex3Unit


class AcousticProcessor:
    def __init__(self, db_path, word_pause_len, synt_pause_len):
        self.__word_pause_len = word_pause_len  # длина паузы между сегментами в синтагме в мс
        self.__syntagma_pause_len = synt_pause_len  # длина паузы между синтагмами в мс
        self.wav_extractor = WavExtractor(db_path, self.__word_pause_len, self.__syntagma_pause_len)

    word_pause_len = property()
    syntagma_pause_len = property()

    def process(self, allophones: [Allophone], mode: int):
        """
        :param allophones
        аллофон, который нужно преобразовать в wav
        :param mode:
            0 -- только аллофон
            1 -- только слоговой комплекс 1-го типа
            2 -- только слоговой комплекс 2-го типа
            3 -- только слоговой комплекс 3-го типа
            4 -- наилучший возможный вариант
        """
        print(allophones)
        final_audio = None
        if mode == 0:
            final_audio = self.__process_allophone(allophones)
        elif mode == 1:
            sc1u = SyllabicComplex1Unit()
            wav = self.__process(sc1u.process_by_word, "AcousticProcessor:process(): syllable-1 not found",
                                 mode, allophones)
            final_audio = wav
        elif mode == 2:
            sc2u = SyllabicComplex2Unit()
            wav = self.__process(sc2u.process_by_word, "AcousticProcessor:process(): syllable-2 not found",
                                 mode, allophones)
            final_audio = wav
        elif mode == 3:
            sc3u = SyllabicComplex3Unit()
            wav = self.__process(sc3u.process_by_word, "AcousticProcessor:process(): syllable-3 not found",
                                 mode, allophones)
            final_audio = wav
        elif mode == 4:
            wav = self.__process_multi_mode(allophones)
            final_audio = wav
        else:
            logging.error("AcousticProcessor:process(): Unknown option")
        return final_audio

    def __process_allophone(self, allophones: [Allophone]) -> AudioSegment:
        final_audio = AudioSegment.empty()
        final_audio += self.wav_extractor.get_wav(allophones, 0)
        return final_audio

    def __process_multi_mode(self, allophones: [Allophone]) -> AudioSegment:
        sc1u = SyllabicComplex1Unit()
        sc2u = SyllabicComplex2Unit()
        sc3u = SyllabicComplex3Unit()
        final_audio = AudioSegment.empty()
        syllables_3 = sc3u.process_by_word(allophones)
        syllables_2 = []
        syllables_1 = []
        for i in range(len(syllables_3)):
            syllables_2.append([])
            for j in range(len(syllables_3[i])):
                s2 = sc2u.process_by_word(syllables_3[i][j])
                syllables_2[i].append(s2[0])

        for i in range(len(syllables_2)):
            syllables_1.append([])
            for j in range(len(syllables_2[i])):
                syllables_1[i].append([])
                for k in range(len(syllables_2[i][j])):
                    s1 = sc1u.process_by_word(syllables_2[i][j][k])
                    syllables_1[i][j].append(s1[0])

        print(syllables_1)
        print(syllables_2)
        print(syllables_3)

        for i in range(len(syllables_3)):
            # units
            for j in range(len(syllables_3[i])):
                # syllables 3 level
                wav = self.wav_extractor.get_wav(syllables_3[i][j], 3)
                if wav is None:
                    for k in range(len(syllables_2[i][j])):
                        # syllables 2 level
                        wav = self.wav_extractor.get_wav(syllables_2[i][j][k], 2)
                        if wav is None:
                            for q in range(len(syllables_1[i][j][k])):
                                # syllables 1 level
                                wav = self.wav_extractor.get_wav(syllables_1[i][j][k][q], 1)
                                if wav is None:
                                    wav = self.wav_extractor.get_wav(syllables_1[i][j][k][q], 0)
                                final_audio += wav
                        else:
                            final_audio += wav
                else:
                    final_audio += wav

        return final_audio

    def __process(self, method, message: str, mode: int, allophones: [Allophone]) -> AudioSegment:
        final_audio = AudioSegment.empty()
        syllables = method(allophones)
        for word in syllables:
            for syllable in word:
                wav = self.wav_extractor.get_wav(syllable, mode)
                if wav is None:
                    logging.warning(message)
                    wav = self.wav_extractor.get_wav(syllable, 0)
                final_audio += wav
        return final_audio

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
