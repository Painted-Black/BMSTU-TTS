from fill_db import fill_db, parse_consonants_pronunciation, parse_stress_string, parse_abbrev_string
from confg import *
from modules.phonetic_processor.phonetic_processor import PhoneticProcessor
from modules.acoustic_processor.acoustic_processor import AcousticProcessor


def load_cons_db():
    fill_db(CONS_FILE_PATH, CONS_DB_NAME, CONS_DB_PATH, parse_consonants_pronunciation)


def load_stress_db():
    fill_db(ZALIZNAK_STRESS_FILE_PATH, STRESS_DB_NAME, STRESS_DB_PATH, parse_stress_string)


def load_abbrev_db():
    fill_db(ABBREV_FILE_PATH, ABBREV_DB_NAME, ABBREV_DB_PATH, parse_abbrev_string)


def main():
    text = "ДА+ЙКА_УГАДА+Ю_КТО+ТО_УКРА+Л_ТВО+Й_СЛА+ДКИЙ_РУЛЕ+Т"
    pt = PhoneticProcessor()
    res = pt.process(text)
    ap = AcousticProcessor("./audio_db/", "./output/out.wav", "wav")
    ap.process(res)
    print(res)


if __name__ == '__main__':
    main()
