from modules.database.db_access_manager import db_access_manager
from confg import *

from nltk import tokenize
from pymorphy2 import MorphAnalyzer
from pymorphy2.tagset import OpencorporaTag
from modules.symbols_base import *
from razdel import sentenize, tokenize
from nltk import word_tokenize
import re
import pickle
import logging


class MorphologicalItem:
    def __init__(self, tag: OpencorporaTag, normal_form: str, item: str, is_abbrev: bool, is_reduction: bool):
        self.item = item
        self.tag = tag
        self.normal_form = normal_form
        self.is_abbrev = is_abbrev
        self.is_reduction = is_reduction

    def __repr__(self):
        return 'MorphologicalItem: item = {0}, tag = {1}, normal_form = {2}'.format(self.item, self.tag, self.normal_form)


class AbbreviationsExtractor:
    abbrev_db_connection = None
    cons_db_connection = None
    AbbreviationsPattern = r"(\b[А-Я]{2,}\b)"

    def init(self) -> bool:
        self.abbrev_db_connection = db_access_manager.create_db(ABBREV_DB_PATH, ABBREV_DB_NAME)
        self.cons_db_connection = db_access_manager.create_db(CONS_DB_PATH, CONS_DB_NAME)
        if self.abbrev_db_connection is None or self.cons_db_connection is None:
            return False
        return True

    def __del__(self):
        if self.abbrev_db_connection is not None:
            self.abbrev_db_connection.close()
        if self.cons_db_connection is not None:
            self.cons_db_connection.close()

    def extract(self, sents: []) -> []:
        return self.__parse_abbrevs(sents)

    def __parse_abbrevs(self, sents):
        if self.abbrev_db_connection is None or self.cons_db_connection is None:
            logging.error('Unable to connect to database {} at {}'.format(ABBREV_DB_NAME, ABBREV_DB_PATH))
            return None
        for sent in sents:
            sent = str(sent)
            res = re.finditer(self.AbbreviationsPattern, sent)
            for match in res:
                abbr = match.group(0)
                # start_idx = match.span(0)[0]
                # end_idx = match.span(0)[1]
                d = self.abbrev_db_connection.read(pickle.dumps(abbr))
                pronunciation = None
                if d is not None:
                    d = pickle.loads(d)
                    definition = self.__chose_abbrev_definition(d)
                    if definition is None:
                        logging.error('Error string in dictionary for abbreviation {0}'.format(abbr))
                        return None
                    pronunciation = definition[0]
                else:
                    pronunciation = self.__pronounce_unknown_abbrev(abbr)
        return sents

    def __pronounce_unknown_abbrev(self, abbr) -> str:
        pronounce = abbr
        if contains_only_consonants(abbr):
            pronounce = self.by_letter(abbr)
        else:
            pronounce = self.__pronounce_abbrev_with_vowel(abbr)

        pronounce = pronounce.lower()
        pronounce = self.stress_last_vowel(pronounce)
        return pronounce

    def __pronounce_abbrev_with_vowel(self, abbrev) -> str:
        if len(abbrev) == 0:
            return abbrev
        pronounce = ''
        if contains_soft_vowel(abbrev):
            if not has_three_more_consonants_in_row(abbrev):
                pronounce = abbrev
            else:
                pronounce = self.mixed_abbrev_pronunciation(abbrev)
        elif is_vowel(abbrev[0]) or is_vowel(abbrev[len(abbrev) - 1]):
            pronounce = self.by_letter(abbrev)
        else:
            if not has_three_more_consonants_in_row(abbrev):
                pronounce = abbrev
            else:
                pronounce = self.by_letter(abbrev)

        return pronounce

    def mixed_abbrev_pronunciation(self, abbrev):
        pronunciation = ''
        flag = False
        for i in range(len(abbrev) - 1, -1, -1):
            if not is_vowel(abbrev[i]):
                if flag is True:
                    pronunciation = abbrev[i] + pronunciation
                else:
                    pronunciation = self.pronounce_letter(abbrev[i]) + pronunciation
                flag = False
            else:
                pronunciation = abbrev[i] + pronunciation
                flag = True
        return pronunciation

    def stress_last_vowel(self, string: str) -> str:
        idx = None
        for i in range(len(string) - 1, -1, -1):
            if is_vowel(string[i]):
                idx = i
                break
        if idx is None:
            logging.warning("No vowels in a word '{}'?".format(string))
            return None
        result = string[:idx + 1]
        result += '+'
        result += string[idx + 1:]
        return result

    def chose_cons_pronunciation(self, pronunciations):
        if len(pronunciations) >= 1:
            if len(pronunciations[0]) >= 1:
                return pronunciations[0][0]
        else:
            return None

    def pronounce_letter(self, letter: str) -> str:
        pronounce = ''
        letter = letter.lower()
        if is_vowel(letter):
            pronounce = letter
            return pronounce
        buff = self.cons_db_connection.read(pickle.dumps(letter))
        if buff is not None:
            buff = pickle.loads(buff)
            pronounce_letter = self.chose_cons_pronunciation(buff)
            if pronounce_letter is None:
                logging.error('Error in dictionary for letter {}'.format(letter))
                return None
            pronounce = pronounce_letter
        else:
            logging.error('Unable to find pronunciation for letter {}'.format(letter))
            return None
        return pronounce

    def by_letter(self, abbr):
        pronounce = ''
        for letter in abbr:
            pronounce_letter = self.pronounce_letter(letter)
            if pronounce_letter is None:
                return None
            pronounce += pronounce_letter
        return pronounce

    def __chose_abbrev_definition(self, definitions):
        if len(definitions) >= 1:
            return definitions[0]
        return None


class SentenceExtractor:
    @staticmethod
    def split_sentences(text: str) -> []:
        buf = sentenize(text)
        buf = list(buf)
        sent = []
        for i in range(len(buf)):
            sent.append([buf[i].text])
        return sent


class WordsExtractor:
    InitialsPattern = r"((\b[А-ЯЁ]\.) *([А-ЯЁ]\b\.)?)"

    def split_words(self, sents: []) -> [[]]:
        sents = self.__split_initials(sents)
        words = []
        for sent in sents:
            sent_words = []
            for sent_part in sent:
                buf = word_tokenize(sent_part)
                for i in range(len(buf)):
                    sent_words.append(buf[i])
            words.append(sent_words)
        return words

    def __split_initials(self, sents: []) -> []:
        for i in range(len(sents)):
            new_sent = []
            for j in range(len(sents[i])):
                sent = sents[i][j]
                split_indexes = []
                res = re.finditer(self.InitialsPattern, sent)
                for match in res:
                    start_idx = match.span(2)[0]
                    end_idx = match.span(2)[1]
                    split_indexes.append(start_idx)
                    split_indexes.append(end_idx)
                    if match.group(3) is not None:
                        start_idx = match.span(3)[0]
                        end_idx = match.span(3)[1]
                        split_indexes.append(start_idx)
                        split_indexes.append(end_idx)
                if len(split_indexes) != 0:
                    split_indexes.insert(0, 0)
                    split_indexes.append(len(sent))
                    for k in range(0, len(split_indexes)-1):
                        start = split_indexes[k]
                        end = split_indexes[k+1]
                        new_part = sent[start:end]
                        if len(new_part) != 0 and not new_part.isspace():
                            new_part = new_part.strip()
                            new_sent.append(new_part)
                else:
                    new_sent.append(sent)
                sents[i] = new_sent
        return sents


class PhoneExtractor:
    def extract(self, text):
        pass


class LinguisticTextProcessor:

    def process(self, text):
        pass
        #text = self.__remove_forbidden_symbols(text)
        #sentences = self.__split_sentences(text)
        #sentences = self.__parse_abbrevs(sentences)
        #words = self.__split_tokens(sentences)
        #words = self.__remove_unnecessary_punctuation_marks(words)
        #return sentences
        #morphs = self.morphological_labeling(words)
        #return morphs
        #words = TextPreprocessingBlock.preprocess(text)
        #print(words)

    def remove_duplicate_spaces(self, text: str) -> str:
        text = text.strip()
        prev_space = False
        new_text = ''
        for i in range(len(text)):
            if text[i] != ' ':
                new_text += text[i]
                prev_space = False
            elif text[i] == ' ' and prev_space == False:
                new_text += text[i]
                prev_space = True
            else: # text[i] == ' ' and prev_space is True:
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
        return text

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
