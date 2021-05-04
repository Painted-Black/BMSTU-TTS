from modules.database.db_access_manager import db_access_manager
from confg import *
from modules.linguistic_processor.abbreviations_extractor import AbbreviationsExtractor
from modules.symbols_base import *
from modules.linguistic_processor.words_extractor import WordsExtractor
from modules.linguistic_processor.sentence_extractor import SentenceExtractor

from pymorphy2 import MorphAnalyzer
from pymorphy2.tagset import OpencorporaTag
import re


class MorphologicalItem:
    def __init__(self, tag: OpencorporaTag, normal_form: str, item: str, is_abbrev: bool, is_reduction: bool):
        self.item = item
        self.tag = tag
        self.normal_form = normal_form
        self.is_abbrev = is_abbrev
        self.is_reduction = is_reduction

    def __repr__(self):
        return 'MorphologicalItem: item = {0}, tag = {1}, normal_form = {2}'.format(self.item, self.tag, self.normal_form)


class LinguisticTextProcessor:
    def __init__(self):
        abbrev_db_connection = db_access_manager.create_db(ABBREV_DB_PATH, ABBREV_DB_NAME)
        cons_db_connection = db_access_manager.create_db(CONS_DB_PATH, CONS_DB_NAME)
        self.__abbrev_extractor = AbbreviationsExtractor(abbrev_db_connection, cons_db_connection)
        self.__word_extractor = WordsExtractor()

    def process(self, text):
        text = self.__remove_forbidden_symbols(text)
        text = self.remove_duplicate_spaces(text)
        sents = SentenceExtractor.split_sentences(text)
        print(sents)
        self.__word_extractor.split_words(sents)
        self.__abbrev_extractor.extract(sents)

        for s in sents:
            print(s.words)

    def remove_duplicate_spaces(self, text: str) -> str:
        text = text.strip()
        prev_space = False
        new_text = ''
        for i in range(len(text)):
            if text[i] != ' ':
                new_text += text[i]
                prev_space = False
            elif text[i] == ' ' and prev_space is False:
                new_text += text[i]
                prev_space = True
            else:  # text[i] == ' ' and prev_space is True:
                prev_space = True
        return new_text

    def __remove_unnecessary_punctuation_marks(self, words):
        for sent in words:
            for word in sent:
                print(word)
        return words

    def __symb_is_permissible(self, symb) -> bool:
        res = False
        res |= any(x == symb for x in RussianLower)
        res |= any(x == symb for x in RussianUpper)
        res |= symb.isdigit()
        res |= any(x == symb for x in PunctuationMarks)
        res |= any(x == symb for x in SpecialReadableSigns)
        return res

    def __remove_forbidden_symbols(self, text: str) -> str:
        new_text = ""
        for i in range(len(text)):
            if self.__symb_is_permissible(text[i]):
                new_text += text[i]
        return new_text

    def morphological_labeling(self, words):
        morph_analyzer = MorphAnalyzer()
        morphs = []
        for word in words:
            morph = morph_analyzer.parse(word)
            print(morph)
            if morph is not None:
                pass
                #morphs.append(MorphologicalItem(morph[0].tag, morph[0].normal_form, word))
        return morphs


DirectSpeechPatterns = [re.compile("((([\"«'])(.+)([\"»'])),( *)([-—])( *)(.+)(\.*!*\?*))"),]  # «П», -а.
