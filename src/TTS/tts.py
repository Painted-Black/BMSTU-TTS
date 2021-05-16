from modules.linguistic_processor.linguistic_text_processor import LinguisticTextProcessor
from modules.prosodic_processor.prosodic_processor import ProsodicProcessor
from modules.acoustic_processor.acoustic_processor import AcousticProcessor
from modules.phonetic_processor.phonetic_processor import PhoneticProcessor

from pydub import AudioSegment
import logging


class TTS:
    def __init__(self, final_audio_path, out_format):
        self.__lp = LinguisticTextProcessor()
        self.__lp.init()
        self.__pp = ProsodicProcessor()
        self.__phop = PhoneticProcessor()
        self.__ap = AcousticProcessor("./audio_db/", 10, 20)
        self.final_audio_path = final_audio_path
        self.out_format = out_format

    def process(self, text: str):
        allophones = []
        audio = AudioSegment.empty()

        sents = self.__lp.process(text)
        syntagmas = self.__pp.process(sents)
        print(syntagmas)
        for synt in syntagmas:
            allophones.append(self.__phop.process(synt))
        for allophone in allophones:
            wav = self.__ap.process(allophone, 4)
            if wav is not None:
                audio += wav
                audio.fade_in(audio.duration_seconds)
            else:
                logging.error("TTS:process(): wav is None")
        audio.set_frame_rate(audio.frame_rate * 2)
        audio.export(self.final_audio_path, format=self.out_format)
