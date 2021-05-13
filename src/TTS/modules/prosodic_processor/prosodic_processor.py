from modules.prosodic_processor.sentence_to_syntagma_converter import SentenceToSyntagmaConverter
from modules.sentence import Sentence


class ProsodicProcessor:
    def __init__(self):
        self.__ssc = SentenceToSyntagmaConverter()

    def process(self, sentences: [Sentence]) -> [str]:
        syntagmas = self.__ssc.convert(sentences)
        return syntagmas
