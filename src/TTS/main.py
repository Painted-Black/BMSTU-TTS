from fill_db import fill_db, parse_consonants_pronunciation, parse_stress_string, parse_abbrev_string
from confg import *
from modules.phonetic_processor import PhoneticProcessor
from modules.phoneme_allophone_transcriptor import PhonemeAllophoneTranscriptor


def load_cons_db():
    fill_db(CONS_FILE_PATH, CONS_DB_NAME, CONS_DB_PATH, parse_consonants_pronunciation)


def load_stress_db():
    fill_db(ZALIZNAK_STRESS_FILE_PATH, STRESS_DB_NAME, STRESS_DB_PATH, parse_stress_string)


def load_abbrev_db():
    fill_db(ABBREV_FILE_PATH, ABBREV_DB_NAME, ABBREV_DB_PATH, parse_abbrev_string)


def main():
    text = "ДО+АРОГО"
    pt = PhonemeAllophoneTranscriptor()
    phonemes = ["a", "a"]
    res = pt.transcript(phonemes)
    #print(res)


if __name__ == '__main__':
    main()
