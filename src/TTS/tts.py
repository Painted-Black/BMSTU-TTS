from modules.linguistic_processor.linguistic_text_processor import LinguisticTextProcessor
from modules.prosodic_processor.prosodic_processor import ProsodicProcessor
from modules.acoustic_processor.acoustic_processor import AcousticProcessor
from modules.phonetic_processor.phonetic_processor import PhoneticProcessor
from PyQt5.QtCore import pyqtSignal, QObject

from pydub import AudioSegment
import logging


class TTS(QObject):
    eventSignal = pyqtSignal(str, int)
    workDone = pyqtSignal()

    def __init__(self, final_audio_path, out_format):
        super().__init__()
        self.__lp = LinguisticTextProcessor()
        self.__lp.init()
        self.__pp = ProsodicProcessor()
        self.__phop = PhoneticProcessor()
        self.__ap = AcousticProcessor("./audio_db/", 10, 20)
        self.final_audio_path = final_audio_path
        self.out_format = out_format

    def process(self, text: str):
        self.eventSignal.emit("Начинаю...", 0)
        allophones = []
        audio = AudioSegment.empty()

        self.eventSignal.emit("Работает лингвистический текстовый процессор...", 16)
        sents = self.__lp.process(text)
        self.eventSignal.emit("Работает просодический процессор...", 32)
        syntagmas = self.__pp.process(sents)
        print(syntagmas)
        self.eventSignal.emit("Работает фонетический процессор...", 48)
        for synt in syntagmas:
            allophones.append(self.__phop.process(synt))

        self.eventSignal.emit("Работает акустический процессор...", 64)
        for allophone in allophones:
            wav = self.__ap.process(allophone, 0)
            if wav is not None:
                audio += wav
                if audio.duration_seconds != 0:
                    audio.fade_in(audio.duration_seconds)
            else:
                logging.error("TTS:process(): wav is None")

        self.eventSignal.emit("Изменяю частоту дискретизации...", 80)
        audio.set_frame_rate(audio.frame_rate * 2)
        audio.export(self.final_audio_path, format=self.out_format)
        self.eventSignal.emit("Готово", 100)
        self.workDone.emit()
