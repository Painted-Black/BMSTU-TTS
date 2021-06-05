from modules.database.db_access_manager import db_access_manager
from confg import *
from modules.linguistic_processor.symbols_base import *
from modules.linguistic_processor.abbreviations_extractor import AbbreviationsExtractor
from modules.linguistic_processor.words_extractor import WordsExtractor
from modules.linguistic_processor.sentence_extractor import SentenceExtractor
from modules.linguistic_processor.phonetix_exceptions_processor import PhonetixExceptionsProcessor
from modules.linguistic_processor.jo_corrector import JoCorrector
from modules.linguistic_processor.stress_marker import StressMarker
from modules.linguistic_processor.morph_tagger import MorphTagger
from modules.linguistic_processor.phonetic_words_formation_unit import PhoneticWordsFormationUnit
from confg import ZALIZNAK_SECONDARY_STRESS_MARK, ZALIZNAK_MAIN_STRESS_MARK
from modules.tts_exceptions.tts_exceptions import WrongPunctuationException, LTPNotInitializedExceprion

import logging

# Тест (предложения) со скобками.


class LinguisticTextProcessor:
    def __init__(self):
        self.__abbrev_extractor = None
        self.__word_extractor = None
        self.__phonetic_except_processor = None
        self.__jo_corrector = None
        self.__stress_marker = None
        self.__morph_tagger = None
        self.__phonetic_words_unit = None

    def valid(self):
        valid = self.__abbrev_extractor is None or \
                self.__word_extractor is None or \
                self.__phonetic_except_processor is None or \
                self.__jo_corrector is None or \
                self.__stress_marker is None or \
                self.__morph_tagger is None or \
                self.__phonetic_words_unit is None
        return not valid

    def init(self) -> bool:
        abbrev_db_connection = db_access_manager.create_db(ABBREV_DB_PATH, ABBREV_DB_NAME)
        cons_db_connection = db_access_manager.create_db(CONS_DB_PATH, CONS_DB_NAME)
        ph_exc_db_connection = db_access_manager.create_db(PH_EXC_DB_PATH, PH_EXC_DB_NAME)
        stress_db_connection = db_access_manager.create_db(STRESS_DB_PATH, STRESS_DB_NAME)
        if abbrev_db_connection is None or cons_db_connection is None or ph_exc_db_connection is None \
                or stress_db_connection is None:
            logging.error("Unable to connect to databases")
            return False
        self.__abbrev_extractor = AbbreviationsExtractor(abbrev_db_connection, cons_db_connection)
        self.__word_extractor = WordsExtractor()
        self.__phonetic_except_processor = PhonetixExceptionsProcessor(ph_exc_db_connection)
        self.__jo_corrector = JoCorrector()
        self.__stress_marker = StressMarker(stress_db_connection, ZALIZNAK_MAIN_STRESS_MARK, ZALIZNAK_SECONDARY_STRESS_MARK)
        self.__morph_tagger = MorphTagger()
        self.__phonetic_words_unit = PhoneticWordsFormationUnit()
        return self.valid()

    def process(self, text):
        if self.valid() is False:
            raise LTPNotInitializedExceprion("Linguistic text processor was not initialized before processing. "
                                             "Call init().")
        text = self.__remove_forbidden_symbols(text)
        text = self.__remove_duplicate_spaces(text)
        sents = SentenceExtractor.split_sentences(text)
        self.__word_extractor.split_words(sents)
        self.__split_hyphen_words(sents)
        self.__mark_tags(sents)
        self.__abbrev_extractor.extract(sents)
        self.__lower_sents(sents)
        self.__correct_jo(sents)
        self.__mark_stress(sents)
        self.__form_phonetic_words(sents)
        self.__upper_phonetic_words(sents)
        return sents

    def __upper_phonetic_words(self, sents):
        for sent in sents:
            words = sent.phonetic_words
            n = len(words)
            for i in range(n):
                words[i] = words[i].upper()
            sent.phonetic_words = words

    def __split_hyphen_words(self, sents):
        for sent in sents:
            new_sent_words = []
            for i in range(len(sent.punct_words)):
                word = sent.punct_words[i]
                if "-" in word:
                    parts = word.split('-')
                    if len(parts) != 2:
                        logging.error("Wrong punctuation in given text")
                        raise WrongPunctuationException("Wrong punctuation in given text")
                    parts[1] = "-" + parts[1]
                    new_sent_words.append(parts[0])
                    new_sent_words.append(parts[1])
                else:
                    new_sent_words.append(word)
            sent.punct_words = new_sent_words

    def __remove_punct_marks(self, words: [str]) -> [str]:
        res = []
        for w in words:
            if w.isalpha() is True:
                res.append(w)
        return res

    def __form_phonetic_words(self, sents: []):
        for s in sents:
            phonetic_s = self.__phonetic_words_unit.form(s.stressed_words, s.tags)
            s.phonetic_words = phonetic_s

    def __mark_tags(self, sents: []):
        for sent in sents:
            tags = self.__morph_tagger.tag(sent.punct_words)
            sent.tags = tags

    def __mark_stress(self, sents):
        for sent in sents:
            stressed_words = self.__stress_marker.mark(sent.punct_words, sent.tags)
            sent.stressed_words = stressed_words

    def __correct_jo(self, sents: []):
        for sent in sents:
            corrected_words = self.__jo_corrector.correct(sent.punct_words)
            sent.words = corrected_words

    def __lower_sents(self, sents: []):
        for sent in sents:
            self.__lower_words(sent.punct_words)
            self.__lower_words(sent.words)

    def __lower_words(self, words: [str]) -> [str]:
        for i in range(len(words)):
            words[i] = words[i].lower()
        return words

    def __remove_duplicate_spaces(self, text: str) -> str:
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
