import pickle
import logging
import re
from modules.symbols_base import *


class AbbreviationsExtractor:
    abbrev_db_connection = None
    cons_db_connection = None
    AbbreviationsPattern = r"(\b[А-Я]{2,}\b)"

    def __init__(self, abbrev_db_connection, cons_db_connection):
        self.abbrev_db_connection = abbrev_db_connection
        self.cons_db_connection = cons_db_connection

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
            n = len(sent.words)
            for i in range(n):
                word = sent.words[i]
                res = re.finditer(self.AbbreviationsPattern, word)
                for match in res:
                    abbr = match.group(0)
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
                    if pronunciation is not None:
                        sent.words[i] = pronunciation
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
